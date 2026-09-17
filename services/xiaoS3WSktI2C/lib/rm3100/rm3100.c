#include "rm3100.h"
#include "esp_log.h"

static const char *TAG = "RM3100";
static i2c_port_t _port;

esp_err_t rm3100_init(i2c_port_t port) {
    _port = port;
    ESP_LOGI(TAG, "RM3100 initialized on I2C port %d", port);
    return ESP_OK;
}

esp_err_t rm3100_read_data(rm3100_data_t *data) {
    if (!data) return ESP_ERR_INVALID_ARG;
    // Stub implementation
    data->x = 123.456f;
    data->y = -23.450f;
    data->z = 987.001f;
    return ESP_OK;
}
