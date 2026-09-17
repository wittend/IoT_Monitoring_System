#ifndef CONFIG_SERVER_H
#define CONFIG_SERVER_H

#include "esp_err.h"

esp_err_t config_server_start(void);
void config_server_stop(void);

#endif // CONFIG_SERVER_H
