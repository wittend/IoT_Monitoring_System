#ifndef RM3100_H
#define RM3100_H

#include "esp_err.h"
#include "driver/i2c.h"

typedef struct {
    float x;
    float y;
    float z;
} rm3100_data_t;

esp_err_t rm3100_init(i2c_port_t port);
esp_err_t rm3100_read_data(rm3100_data_t *data);

#endif // RM3100_H
