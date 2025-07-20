#include <esp_now.h>
#include <WiFi.h>

typedef struct {
  bool jump;
  bool duck;
} input_message;

typedef struct {
  int db;
} test_message;

input_message outgoing;
test_message test;

uint8_t gameMAC[] = {0x3C, 0x84, 0x27, 0xC2, 0xDF, 0x90};

void onReceive(const uint8_t *mac, const uint8_t *data, int len) {
  memcpy(&test, data, sizeof(test_message));
  Serial.println(test.db);
}

void setup() {
  Serial.begin(9600);

  // ESP-NOW establishment
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, gameMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (!esp_now_is_peer_exist(gameMAC)) {
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
      Serial.println("Failed to add peer");
    }
  }
  
  esp_now_register_recv_cb(onReceive);

  outgoing.jump = true;
  outgoing.duck = true;
}

void loop() {
  esp_now_send(gameMAC, (uint8_t *)&outgoing, sizeof(outgoing)); 
}
