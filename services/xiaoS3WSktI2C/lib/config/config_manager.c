#include "config_manager.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "CONFIG";
static const char *NVS_NAMESPACE = "storage";
static const char *CONFIG_KEY = "device_cfg";

esp_err_t config_init(void) {
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    return err;
}

esp_err_t config_load(device_config_t *config) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE, NVS_READONLY, &handle);
    if (err != ESP_OK) {
        config_reset_to_defaults(config);
        return err;
    }
    size_t size = sizeof(device_config_t);
    err = nvs_get_blob(handle, CONFIG_KEY, config, &size);
    nvs_close(handle);
    if (err != ESP_OK) {
        config_reset_to_defaults(config);
    }
    return err;
}

esp_err_t config_save(const device_config_t *config) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open(NVS_NAMESPACE, NVS_READWRITE, &handle);
    if (err != ESP_OK) return err;
    err = nvs_set_blob(handle, CONFIG_KEY, config, sizeof(device_config_t));
    if (err == ESP_OK) {
        err = nvs_commit(handle);
    }
    nvs_close(handle);
    return err;
}

void config_reset_to_defaults(device_config_t *config) {
    memset(config, 0, sizeof(device_config_t));
    strncpy(config->node_id, "node-001", sizeof(config->node_id));
    config->latitude = 0.0;
    config->longitude = 0.0;
    config->elevation = 0.0;
    strncpy(config->owner, "unassigned", sizeof(config->owner));
    strncpy(config->orientation, "north", sizeof(config->orientation));
    config->frequency = 868100000;
    config->sf = 7;
    config->bw = 125000;
}
