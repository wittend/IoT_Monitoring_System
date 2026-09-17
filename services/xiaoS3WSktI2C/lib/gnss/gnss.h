#ifndef GNSS_H
#define GNSS_H

#include "esp_err.h"

esp_err_t gnss_init(void);
esp_err_t gnss_get_time(char *ts_buffer, size_t size);

#endif // GNSS_H
