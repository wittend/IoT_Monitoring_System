#include "comm_manager.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "driver/gpio.h"
#include <string.h>

#define CONFIG_MODE_GPIO 0  // Boot button on XIAO ESP32S3 is often GPIO 0
static const char *TAG = "COMM";

esp_err_t comm_init(void) {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << CONFIG_MODE_GPIO),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };
    gpio_config(&io_conf);
    
    return ESP_OK;
}

esp_err_t comm_wifi_ap_start(void) {
    esp_netif_create_default_wifi_ap();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    
    wifi_config_t wifi_config = {
        .ap = {
            .ssid = "XIAO_S3_CONFIG",
            .ssid_len = strlen("XIAO_S3_CONFIG"),
            .channel = 1,
            .password = "",
            .max_connection = 4,
            .authmode = WIFI_AUTH_OPEN
        },
    };
    
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
    
    ESP_LOGI(TAG, "WiFi AP started. SSID: XIAO_S3_CONFIG");
    return ESP_OK;
}

void comm_wifi_stop(void) {
    esp_wifi_stop();
    esp_wifi_deinit();
}

bool comm_check_config_mode_trigger(void) {
    // Check if button is pressed (LOW)
    return gpio_get_level(CONFIG_MODE_GPIO) == 0;
}
