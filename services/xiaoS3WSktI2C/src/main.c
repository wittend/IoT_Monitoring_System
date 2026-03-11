#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include "rm3100.h"
#include "mcp9808.h"
#include "sx1262.h"
#include "gnss.h"
#include "config_manager.h"
#include "comm_manager.h"
#include "config_server.h"

static const char *TAG = "APP";
static device_config_t g_config;

#define I2C_MASTER_SCL_IO           7       // Seeed XIAO S3 SCL (D5)
#define I2C_MASTER_SDA_IO           6       // Seeed XIAO S3 SDA (D4)
#define I2C_MASTER_NUM              I2C_NUM_0
#define I2C_MASTER_FREQ_HZ          100000
#define I2C_MASTER_TX_BUF_DISABLE   0
#define I2C_MASTER_RX_BUF_DISABLE   0

static esp_err_t i2c_master_init(void) {
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };
    esp_err_t err = i2c_param_config(I2C_MASTER_NUM, &conf);
    if (err != ESP_OK) return err;
    return i2c_driver_install(I2C_MASTER_NUM, conf.mode, I2C_MASTER_TX_BUF_DISABLE, I2C_MASTER_RX_BUF_DISABLE, 0);
}

void sensor_task(void *pvParameters) {
    char ts[32];
    rm3100_data_t mag_data;
    float temp;
    char jsonl_buf[256];
    TickType_t start_tick = xTaskGetTickCount();

    while (1) {
        // REQ-001: Sample sensors once per second
        gnss_get_time(ts, sizeof(ts));
        rm3100_read_data(&mag_data);
        mcp9808_read_temp(&temp);

        // REQ-003: Format as JSONL
        // Format: { "ts":"26 Oct 2025 14:20:00", "rt": 25.000, "x":12345.678, "y":-234.500, "z":987.001 }
        snprintf(jsonl_buf, sizeof(jsonl_buf),
                 "{\"ts\":\"%s\", \"rt\":%.3f, \"x\":%.3f, \"y\":%.3f, \"z\":%.3f}",
                 ts, temp, mag_data.x, mag_data.y, mag_data.z);

        // REQ-001: Send data
        printf("%s\n", jsonl_buf);
        sx1262_send(jsonl_buf);

        // Maintain 1Hz cadence
        vTaskDelayUntil(&start_tick, pdMS_TO_TICKS(1000));
    }
}

void app_main(void) {
    ESP_LOGI(TAG, "Starting XIAO ESP32S3 Edge Data Collector...");

    // Initialize NVS and Load Config
    ESP_ERROR_CHECK(config_init());
    config_load(&g_config);

    // Initialize Comm (WiFi/Event Loop/GPIO)
    ESP_ERROR_CHECK(comm_init());

    // Check for Config Mode Trigger
    if (comm_check_config_mode_trigger()) {
        ESP_LOGI(TAG, "Entering Configuration Mode...");
        ESP_ERROR_CHECK(comm_wifi_ap_start());
        ESP_ERROR_CHECK(config_server_start());
        // In config mode, we stay here until restart
        return;
    }

    // Initialize I2C
    ESP_ERROR_CHECK(i2c_master_init());

    // Initialize drivers
    ESP_ERROR_CHECK(rm3100_init(I2C_MASTER_NUM));
    ESP_ERROR_CHECK(mcp9808_init(I2C_MASTER_NUM));
    ESP_ERROR_CHECK(sx1262_init());
    ESP_ERROR_CHECK(gnss_init());

    // Create sensor sampling task
    xTaskCreate(sensor_task, "sensor_task", 4096, NULL, 5, NULL);
}
