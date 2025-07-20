#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>

typedef struct {
  bool jump;
  bool duck;
} input_message;

typedef struct {
  int db;
} test_message;

input_message incoming;
test_message test;

volatile int8_t lastRSSI = 0;

uint8_t inputMAC[] = {0x74, 0x4D, 0xBD, 0xA2, 0x0D, 0x38};

void promiscuous_rx_cb(void* buf, wifi_promiscuous_pkt_type_t type) {
  if (type != WIFI_PKT_MGMT && type != WIFI_PKT_DATA) return;

  wifi_promiscuous_pkt_t* pkt = (wifi_promiscuous_pkt_t*) buf;
  lastRSSI = pkt->rx_ctrl.rssi;
}

void onReceive(const uint8_t *mac, const uint8_t *data, int len) {
  memcpy(&incoming, data, sizeof(input_message));
 
  test.db = lastRSSI;
  esp_now_send(inputMAC, (uint8_t *)&test, sizeof(test));
  
}

void setup() {
  Serial.begin(9600);

  // ESP-NOW establishment
  WiFi.mode(WIFI_STA);
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_rx_cb(&promiscuous_rx_cb);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, inputMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (!esp_now_is_peer_exist(inputMAC)) {
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
      Serial.println("Failed to add peer");
    }
  }

  esp_now_register_recv_cb(onReceive);
}

void loop() {
  
}
