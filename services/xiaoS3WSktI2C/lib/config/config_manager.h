#ifndef CONFIG_MANAGER_H
#define CONFIG_MANAGER_H

#include "esp_err.h"

typedef struct {
    char node_id[32];
    double latitude;
    double longitude;
    double elevation;
    char owner[64];
    char orientation[32];
    // LoRa params
    long frequency;
    int sf;
    int bw;
} device_config_t;

esp_err_t config_init(void);
esp_err_t config_load(device_config_t *config);
esp_err_t config_save(const device_config_t *config);
void config_reset_to_defaults(device_config_t *config);

#endif // CONFIG_MANAGER_H
