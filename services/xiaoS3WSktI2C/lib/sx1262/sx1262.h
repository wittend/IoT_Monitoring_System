#ifndef SX1262_H
#define SX1262_H

#include "esp_err.h"

esp_err_t sx1262_init(void);
esp_err_t sx1262_send(const char *payload);

#endif // SX1262_H
