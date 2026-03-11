#include "mcp9808.h"
#include "esp_log.h"

static const char *TAG = "MCP9808";
static i2c_port_t _port;

esp_err_t mcp9808_init(i2c_port_t port) {
    _port = port;
    ESP_LOGI(TAG, "MCP9808 initialized on I2C port %d", port);
    return ESP_OK;
}

esp_err_t mcp9808_read_temp(float *temp) {
    if (!temp) return ESP_ERR_INVALID_ARG;
    // Stub implementation
    *temp = 25.0f;
    return ESP_OK;
}
