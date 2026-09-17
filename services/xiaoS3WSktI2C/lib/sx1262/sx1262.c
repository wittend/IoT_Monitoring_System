#include "sx1262.h"
#include "esp_log.h"

static const char *TAG = "SX1262";

esp_err_t sx1262_init(void) {
    ESP_LOGI(TAG, "SX1262 LoRa module initialized");
    return ESP_OK;
}

esp_err_t sx1262_send(const char *payload) {
    ESP_LOGI(TAG, "Sending LoRa payload: %s", payload);
    return ESP_OK;
}
