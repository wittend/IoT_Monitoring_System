#include "config_server.h"
#include "config_manager.h"
#include "esp_http_server.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include <string.h>

static const char *TAG = "CFG_SRV";

static esp_err_t config_get_handler(httpd_req_t *req) {
    device_config_t config;
    config_load(&config);

    char html[2048];
    snprintf(html, sizeof(html),
        "<html><body><h1>Device Configuration</h1>"
        "<form method='POST' action='/save'>"
        "Node ID: <input type='text' name='node_id' value='%s'><br>"
        "Latitude: <input type='text' name='latitude' value='%.6f'><br>"
        "Longitude: <input type='text' name='longitude' value='%.6f'><br>"
        "Elevation: <input type='text' name='elevation' value='%.2f'><br>"
        "Owner: <input type='text' name='owner' value='%s'><br>"
        "Orientation: <input type='text' name='orientation' value='%s'><br>"
        "<input type='submit' value='Save'>"
        "</form></body></html>",
        config.node_id, config.latitude, config.longitude, config.elevation, config.owner, config.orientation
    );
    httpd_resp_send(req, html, HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t config_post_handler(httpd_req_t *req) {
    char buf[512];
    int ret, remaining = req->content_len;
    if (remaining > sizeof(buf) - 1) return ESP_FAIL;
    ret = httpd_req_recv(req, buf, remaining);
    if (ret <= 0) return ESP_FAIL;
    buf[ret] = '\0';

    ESP_LOGI(TAG, "Received post data: %s", buf);
    // Note: In a real app, you'd parse url-encoded parameters here.
    // Stub implementation for now.
    
    httpd_resp_sendstr(req, "Configuration saved. Restarting...");
    vTaskDelay(pdMS_TO_TICKS(1000));
    esp_restart();
    return ESP_OK;
}

static httpd_uri_t uri_get = {
    .uri      = "/",
    .method   = HTTP_GET,
    .handler  = config_get_handler,
    .user_ctx = NULL
};

static httpd_uri_t uri_post = {
    .uri      = "/save",
    .method   = HTTP_POST,
    .handler  = config_post_handler,
    .user_ctx = NULL
};

static httpd_handle_t server = NULL;

esp_err_t config_server_start(void) {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_register_uri_handler(server, &uri_get);
        httpd_register_uri_handler(server, &uri_post);
        return ESP_OK;
    }
    return ESP_FAIL;
}

void config_server_stop(void) {
    if (server) {
        httpd_stop(server);
        server = NULL;
    }
}
