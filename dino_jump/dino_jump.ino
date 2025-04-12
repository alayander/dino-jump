#include "bit_array_2d.hpp"
#include "game.hpp"
#include "hologram_fan.hpp"
#include "title_frame.hpp"

/* Display Pins */
#define RESET_PIN D7
#define PROXIMITY_PIN D8
#define BEAM_BREAK_PIN D9

/* Base ESP32 Pins */
#define BASE_INPUT0_PIN D10
#define BASE_INPUT1_PIN D11
#define BASE_OUTPUT_PIN D12


enum State {
  IDLE,
  TITLE,
  GAME,
  DEATH,
};


Game game;
HologramFan display;
State currentState = IDLE;
bool advance = false;
bool jumped = false;
bool timedout = false;


void setup() {
  Wire.begin();
  Wire.setClock(800000);

  pinMode(PROXIMITY_PIN, INPUT);
  pinMode(BEAM_BREAK_PIN, INPUT_PULLUP);

  pinMode(BASE_INPUT0_PIN, INPUT);
  pinMode(BASE_INPUT1_PIN, INPUT);
  pinMode(BASE_OUTPUT_PIN, OUTPUT);

  pinMode(RESET_PIN, OUTPUT);
  digitalWrite(RESET_PIN, LOW);
  delay(5);
  digitalWrite(RESET_PIN, HIGH);

  display.begin();

  attachInterrupt(digitalPinToInterrupt(BASE_INPUT1_PIN), handle_jump, RISING);
}

void loop() {
  title_loop();
//  switch (currentState) {
//    case IDLE:
//      idle_loop();
//      break;
//    case TITLE: 
//      title_loop();
//      break;
//    case GAME:
//      game_loop();
//      break;
//    case DEATH:
//      death_loop();
//      break;
//  }
}

void idle_loop() {
  attachInterrupt(digitalPinToInterrupt(BASE_INPUT0_PIN), handle_state_input, RISING);
  advance = false;
  
  while (!advance) {
  }
  currentState = TITLE;
}

void title_loop() {
  advance = false;
  timedout = false;
  
  while (!advance && !timedout) {
    if (jumped) {
      jumped = false;
      timedout = true;
    }
    
    if (digitalRead(PROXIMITY_PIN) == LOW) {
      display.flash_frame(TITLE_FRAME, digitalRead(BEAM_BREAK_PIN) == HIGH ? 1 : 0);
    }
    delay(1);
  }

  if (timedout) {
    currentState = IDLE;
  } else {
    currentState = GAME;
  }
}

void game_loop() {
  detachInterrupt(digitalPinToInterrupt(BASE_INPUT0_PIN));
  
  while (!game.get_collision()) {
    if (digitalRead(PROXIMITY_PIN) == LOW) {
      display.flash_frame(game.get_frame(), digitalRead(BEAM_BREAK_PIN) == HIGH ? 1 : 0);
  
      if (jumped) {
        game.input(Input_State::JUMP);
        jumped = false;
      } else if (digitalRead(BASE_INPUT0_PIN) == HIGH) {
        game.input(Input_State::DUCK);
      } else {
        game.input(Input_State::NEUTRAL);
      }
      game.update_obstacles();
      game.update_frame();
    }
    delay(1);
  }
  currentState = DEATH;
}

void death_loop() {
  unsigned long death_screen_start = millis();
  while (millis() - death_screen_start < 10000) {
    display.flash_frame(game.get_frame(), digitalRead(BEAM_BREAK_PIN) == HIGH ? 1 : 0);
  }

  // Communicate game over to Base
  digitalWrite(BASE_OUTPUT_PIN, HIGH);
  digitalWrite(BASE_OUTPUT_PIN, LOW);

  currentState = TITLE;
}

void handle_state_input() {
  advance = true;
}

void handle_jump() {
  jumped = true;
}
