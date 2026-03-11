#ifndef MCP9808_H
#define MCP9808_H

#include "esp_err.h"
#include "driver/i2c.h"

esp_err_t mcp9808_init(i2c_port_t port);
esp_err_t mcp9808_read_temp(float *temp);

#endif // MCP9808_H
