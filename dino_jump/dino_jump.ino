#include "bit_array_2d.hpp"
#include "game.hpp"
#include "hologram_fan.hpp"
#include "title_frame.hpp"

#include <esp_now.h>
#include <WiFi.h>

/* Display Pins */
#define RESET_PIN D7
#define BEAM_BREAK_PIN D9

/* Base ESP32 Pins */
#define BASE_INPUT0_PIN D10 // DUCK (Green)
#define BASE_INPUT1_PIN D11 // JUMP (Orange)
#define BASE_OUTPUT_PIN D12 // DEATH (Yellow)

#define LED_BUILTIN 13

enum State {
  IDLE,
  TITLE,
  GAME,
  DEATH,
};

const unsigned long MAX_EXPECTED_PERIOD = 350;
const unsigned long DEATH_SCREEN_PERIOD = 5000;

typedef struct {
  bool jump;
  bool duck;
} input_message;

input_message incoming;

uint8_t inputMAC[] = {0x74, 0x4D, 0xBD, 0xA2, 0x0D, 0x38};

Game game;
HologramFan display;
State currentState = IDLE;
bool advance = false;
bool jumped = false;
bool ducked = false;
bool timedout = false;
bool beam_break_rising = false;


void onReceive(const uint8_t *mac, const uint8_t *data, int len) {
  memcpy(&incoming, data, sizeof(incoming));
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.print(incoming.jump);
  Serial.print(" ");
  Serial.println(incoming.duck);
  digitalWrite(LED_BUILTIN, LOW);
}

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.setClock(800000);

  // pin initialization
  pinMode(BEAM_BREAK_PIN, INPUT_PULLUP);

  pinMode(BASE_INPUT0_PIN, INPUT);
  pinMode(BASE_INPUT1_PIN, INPUT);
  pinMode(BASE_OUTPUT_PIN, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(RESET_PIN, OUTPUT);
  digitalWrite(RESET_PIN, LOW);
  delay(5);
  digitalWrite(RESET_PIN, HIGH);

  display.begin();

  digitalWrite(BASE_OUTPUT_PIN, LOW);
  attachInterrupt(digitalPinToInterrupt(BEAM_BREAK_PIN), handle_beam_break_rising, RISING);

  // ESP-NOW establishment
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  delay(10000);

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
 Serial.println("loop");
 switch (currentState) {
   case IDLE:
     Serial.println("idle");
     idle_loop();
     break;
   case TITLE: 
     Serial.println("title");
     title_loop();
     break;
   case GAME:
     Serial.println("game");
     game_loop();
     break;
   case DEATH:
     Serial.println("death");
     death_loop();
     break;
 }
}

void idle_loop() {
  attachInterrupt(digitalPinToInterrupt(BASE_INPUT0_PIN), handle_state_input, RISING);
  advance = false;
  
  while (!advance) {
    Serial.println("not advancing, still idle");
  }
  currentState = TITLE;
  detachInterrupt(digitalPinToInterrupt(BASE_INPUT0_PIN));
}

void title_loop() {
  attachInterrupt(digitalPinToInterrupt(BASE_INPUT0_PIN), handle_state_input, RISING);
  attachInterrupt(digitalPinToInterrupt(BASE_INPUT1_PIN), handle_jump, RISING);
  beam_break_rising = false;

  advance = false;
  timedout = false;

  unsigned long prev = 0;
  unsigned long curr = millis();
  unsigned long time_passed = 0;
  while (!advance && !timedout) {
    if (beam_break_rising) {
      bool first_time = prev == 0;
      curr = millis();
      time_passed = curr - prev;
      prev = curr;

      // Skip first time as time_passed is not a valid value
      if (first_time) {
        continue;
      }
      display.flash_frame(LINE_TITLE_FRAME, 1);

      if (time_passed < MAX_EXPECTED_PERIOD) {
        unsigned long next_flash_time = curr + time_passed / 2;
        while (millis() < next_flash_time);
        display.flash_frame(TITLE_LINE_FRAME, 0);
      }

      beam_break_rising = false;
    }

    if (jumped) {
      jumped = false;
      timedout = true;
    }
    
    delay(1);
  }

  if (timedout) {
    currentState = IDLE;
  } else {
    currentState = GAME;
  }
  detachInterrupt(digitalPinToInterrupt(BASE_INPUT0_PIN));
  detachInterrupt(digitalPinToInterrupt(BASE_INPUT1_PIN));
}

void game_loop() {
  attachInterrupt(digitalPinToInterrupt(BASE_INPUT1_PIN), handle_jump, RISING);
  beam_break_rising = false;

  Game curr_game;
  
  unsigned long prev = 0;
  unsigned long curr = millis();
  unsigned long time_passed = 0;
  while (!curr_game.get_collision()) {
    Serial.println("Game loop");
    if (beam_break_rising) {
      bool first_time = prev == 0;
      curr = millis();
      time_passed = curr - prev;
      prev = curr;

      // Skip first time as time_passed is not a valid value
     Serial.println("death");
      if (first_time) {
        continue;
      }
      display.flash_frame(curr_game.get_frame(), 1);
  
      if (incoming.jump) {
        curr_game.input(Input_State::JUMP);
      } else if (incoming.duck) {
        curr_game.input(Input_State::DUCK);
      } else {
        curr_game.input(Input_State::NEUTRAL);
      }
      curr_game.update_obstacles();
      curr_game.update_frame();


      if (time_passed < MAX_EXPECTED_PERIOD) {
        unsigned long next_flash_time = curr + time_passed / 2;
        while (millis() < next_flash_time);
        display.flash_frame(curr_game.get_frame(), 0);

      }

      // Update game regardless of flashing as we don't want to slow down the game
      if (incoming.jump) {
        curr_game.input(Input_State::JUMP);
      } else if (incoming.duck) {
        curr_game.input(Input_State::DUCK);
      } else {
        curr_game.input(Input_State::NEUTRAL);
      }
      curr_game.update_obstacles();
      curr_game.update_frame();

      beam_break_rising = false;
    }
    digitalWrite(BASE_OUTPUT_PIN, LOW);
    delay(1);
  }

  Serial.println("Collision occured");
  game = curr_game;
  currentState = DEATH;
  detachInterrupt(digitalPinToInterrupt(BASE_INPUT1_PIN));
}

void death_loop() {
  beam_break_rising = false;

  unsigned long prev = 0;
  unsigned long curr = millis();
  unsigned long time_passed = 0;
  unsigned long death_screen_start = millis();
  while (millis() - death_screen_start < DEATH_SCREEN_PERIOD) {
    if (beam_break_rising) {
      bool first_time = prev == 0;
      curr = millis();
      time_passed = curr - prev;
      prev = curr;

      // Skip first time as time_passed is not a valid value
      if (first_time) {
        continue;
      }
      display.flash_frame(game.get_frame(), 1);

      if (time_passed < MAX_EXPECTED_PERIOD) {
        unsigned long next_flash_time = curr + time_passed / 2;
        while (millis() < next_flash_time);
        display.flash_frame(game.get_frame(), 0);

      }

      beam_break_rising = false;
    }
  }

  // Communicate game over to Base
  digitalWrite(BASE_OUTPUT_PIN, HIGH);
  delay(5);
  digitalWrite(BASE_OUTPUT_PIN, LOW);

  currentState = TITLE;
}

void handle_state_input() {
  advance = true;
}

void handle_jump() {
  jumped = true;
}

void handle_beam_break_rising() {
  beam_break_rising = true;
}
