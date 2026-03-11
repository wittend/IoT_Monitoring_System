#include "gnss.h"
#include "esp_log.h"
#include <time.h>
#include <string.h>

static const char *TAG = "GNSS";

esp_err_t gnss_init(void) {
    ESP_LOGI(TAG, "GNSS module initialized on UART");
    return ESP_OK;
}

esp_err_t gnss_get_time(char *ts_buffer, size_t size) {
    if (!ts_buffer) return ESP_ERR_INVALID_ARG;
    // Stub implementation: RFC-2822-like timestamp
    // Format: DD Mon YYYY HH:MM:SS
    time_t now = time(NULL);
    struct tm timeinfo;
    gmtime_r(&now, &timeinfo);
    strftime(ts_buffer, size, "%d %b %Y %H:%M:%S", &timeinfo);
    return ESP_OK;
}
