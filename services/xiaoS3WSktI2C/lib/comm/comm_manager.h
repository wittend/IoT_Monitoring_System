#ifndef COMM_MANAGER_H
#define COMM_MANAGER_H

#include "esp_err.h"
#include <stdbool.h>

esp_err_t comm_init(void);
esp_err_t comm_wifi_ap_start(void);
void comm_wifi_stop(void);
bool comm_check_config_mode_trigger(void);

#endif // COMM_MANAGER_H
