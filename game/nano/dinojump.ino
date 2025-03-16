//////////////////////////////////////////////////////////////////////////////

// Imports
#include "Adafruit_LEDBackpack.h"
#include "game.hpp"
#include "terminal_display.hpp"
#include <Adafruit_GFX.h>
#include <Wire.h>
#include <atomic>
#include <iostream>
#include <mutex>
#include <thread>

// Constants for button GPIO pins
#define START_GAME 2  // Start Game Button
#define END_GAME 3    // Stop Game Button
#define JUMP_BUTTON 4 // Jump Button
#define DUCK_BUTTON 5 // Duck Button

// Adafruit backpacks setup
Adafruit_LEDBackpack display1 = Adafruit_LEDBackpack(); // Hex Display 1
Adafruit_LEDBackpack display2 = Adafruit_LEDBackpack(); // Hex Display 2

// Inital game class and states
Game game;
std::atomic<bool> quit{false};       // Flag to signal quitting the game
std::atomic<bool> gameActive{false}; // Flag to signal if the game is active
std::atomic<bool> game_over{false};  // Flag to signal game over
std::atomic<bool> maxUpdated{false}; // Flag to signal if max score was updated

// Other game constants
const int SPEED = 10000; // Delay speed in game loop
uint16_t count = 0;      // Counter for display 1
uint16_t maxCount = 0;   // Highest value stored in display 2

//////////////////////////////////////////////////////////////////////////////

// Function to handle player input and update game actions
void player_input(Input_State input) {
  if (!game_over) {
    game.input(input);
  }
}

// Prints the compressed frame data to the serial monitor
void print_compressed_frame(Frame frame) {
  char buf[MAX_X * 13 + 1] = {0};
  frame.compressed_form(buf);
  Serial.println(buf);
}

// HEX representation of digits for 7-segment display
const uint16_t digitToSegment[10] = {0x3F, 0x06, 0x5B, 0x4F, 0x66,
                                     0x6D, 0x7D, 0x07, 0x7F, 0x6F};

// Function to display a number on the hex display
void displayNumber(Adafruit_LEDBackpack &matrix, int number) {
  // Serial.println(number);
  matrix.clear();
  if (number < 0 || number > 9999)
    return; // Ensure number is within range
  int counts[4] = {0, 1, 3, 4};
  for (int i = 3; i >= 0; i--) {
    int digit = number % 10;
    matrix.displaybuffer[counts[i]] = digitToSegment[digit];
    number /= 10;
  }
  matrix.writeDisplay();
}

// Function to display countdown on the hex display
void displayCountdown(Adafruit_LEDBackpack &matrix, int number) {
  // Serial.println(number);
  matrix.clear();
  matrix.displaybuffer[1] = digitToSegment[number];
  matrix.writeDisplay();
}

//////////////////////////////////////////////////////////////////////////////

void setup() {
  // Initialize serial communication and button pins
  Serial.begin(9600);
  pinMode(START_GAME, INPUT_PULLUP);
  pinMode(END_GAME, INPUT_PULLUP);
  pinMode(JUMP_BUTTON, INPUT_PULLUP);
  pinMode(DUCK_BUTTON, INPUT_PULLUP);
  // Setup everything for the Display
  display1.begin(0x70);       // Initialize Display 1
  display2.begin(0x71);       // Initialize Display 2
  displayNumber(display1, 0); // Set initial score display to 0
  displayNumber(display2, 0); // Set initial max score display to 0
  Serial.println("Setup Complete");
}

void loop() {
  // Handle the Start Game Button input
  int start_state = digitalRead(START_GAME);
  if (start_state == HIGH && !gameActive) {
    game = Game(); // Start a new game
    gameActive = true;
    game_over = false;
    maxUpdated = false;
    // Run a 3 2 1 countdown
    int countdownValue = 3;
    while (countdownValue > 0) {
      displayCountdown(display1, countdownValue);
      countdownValue--;
      delay(1200);
    }
    Serial.println("Game Started!");
  }
  // If the game is active and hasn't ended, handle player input and update the
  // game state
  if (gameActive && !game_over) {
    // Read all inputs
    int jump_state = digitalRead(JUMP_BUTTON);
    int duck_state = digitalRead(DUCK_BUTTON);
    int quit_state = digitalRead(END_GAME);
    // Send inputs
    if (jump_state == HIGH) {
      player_input(JUMP);
    } else if (duck_state == HIGH) {
      player_input(DUCK);
    } else if (quit_state == HIGH) {
      game_over = true;
      gameActive = false;
    }
    // Update logic and frame
    game.update_obstacles();
    game.update_frame();
    print_compressed_frame(game.get_frame());
    // Update game score
    count = game.get_score();
    displayNumber(display1, count);
    // Short delay
    delay(SPEED / 1000);
  }
  // Once the game is over, update the max and wait for another game to start
  if (game_over && !maxUpdated) {
    Serial.println("Game Over!");
    if (count > maxCount) {
      maxCount = count; // Update max score if current score is higher
      displayNumber(display2, maxCount); // Display max score on Display 2
      Serial.println("Updated Max!");
    }
    maxUpdated = true; // Next iteration, we don't update max again
    delay(500);        // Have a short wait
    count = 0;         // Reset score display
    displayNumber(display1, count);
  }
}

//////////////////////////////////////////////////////////////////////////////

// #include "game.hpp"
// #include "terminal_display.hpp"
// #include <atomic>
// #include <iostream>
// #include <mutex>
// #include <thread>

// // Constants for button GPIO pins
// #define START_GAME 2  // Start Game Button
// #define END_GAME 3    // Stop Game Button
// #define JUMP_BUTTON 4  // Jump Button
// #define DUCK_BUTTON 5  // Duck Button

// const int SPEED = 10000;  // Delay speed in game loop

// Game game;
// std::atomic<bool> quit{false};  // Flag to signal quitting the game
// std::atomic<bool> gameActive{false};  // Flag to signal if the game is active
// std::atomic<bool> game_over{false};  // Flag to signal game over

// void setup() {
//     // Initialize serial communication and button pins
//     // Serial.begin(115200);
//     Serial.begin(9600);
//     pinMode(START_GAME, INPUT_PULLUP);
//     pinMode(END_GAME, INPUT_PULLUP);
//     pinMode(JUMP_BUTTON, INPUT_PULLUP);
//     pinMode(DUCK_BUTTON, INPUT_PULLUP);
//     Serial.println("Setup Complete");
// }

// // Function to handle player input and update game actions
// void player_input(Input_State input) {
//     if (!game_over) {
//         game.input(input);
//     }
// }

// void print_compressed_frame(Frame frame) {
//     char buf[MAX_X * 13 + 1] = {0};
//     frame.compressed_form(buf);
//     Serial.println(buf);
// }

// void loop() {
//     // Handle the Start Game Button input
//     int start_state = digitalRead(START_GAME);
//     if (start_state == HIGH && !gameActive) {
//         // Start a new game
//         game = Game();
//         gameActive = true;
//         game_over = false;
//         Serial.println("Game Started!");
//     }

//     // If the game is active and hasn't ended, handle player input and update
//     the game state if (gameActive && !game_over) {
//         int jump_state = digitalRead(JUMP_BUTTON);
//         int duck_state = digitalRead(DUCK_BUTTON);
//         int quit_state = digitalRead(END_GAME);

//         // Handle player input based on button presses
//         if (jump_state == HIGH) {
//             player_input(JUMP);
//             // Serial.println("Jump!");
//         } else if (duck_state == HIGH) {
//             player_input(DUCK);
//             // Serial.println("Duck!");
//         } else if (quit_state == HIGH) {
//             game_over = true;
//             gameActive = false;
//             // Serial.println("Game Stopped!");
//         }

//         // // Update game logic and frame
//         game.update_obstacles();
//         game.update_frame();
//         print_compressed_frame(game.get_frame());
//         // Serial.println("frame");
//         // delay(50);
//         delay(SPEED / 1000);  // Add a delay (in milliseconds)
//     }

//     // If the game is over, print the game over message
//     if (game_over) {
//         Serial.println("Game Over!");
//         // Serial.println("Score");
//     }
// }

// #include "game.hpp"
// #include "terminal_display.hpp"
// #include <atomic>
// #include <iostream>
// #include <mutex>
// #include <thread>

// const int SPEED = 10000;  // Delay speed in game loop

// Game game;

// // Constants for button GPIO pins
// const int BUTTON_JUMP_PIN = 12;
// const int BUTTON_DUCK_PIN = 13;
// const int BUTTON_QUIT_PIN = 14;

// std::atomic<bool> quit{false};  // Flag to signal quitting the game
// std::atomic<bool> game_over{false};  // Flag to signal game over

// // Function for handling input from the buttons
// void input_thread_func() {
//     while (!game_over) {
//         // Read button states
//         int jump_state = digitalRead(BUTTON_JUMP_PIN);
//         int duck_state = digitalRead(BUTTON_DUCK_PIN);
//         int quit_state = digitalRead(BUTTON_QUIT_PIN);

//         // Store button states, each button corresponds to a different key
//         press action if (jump_state == HIGH) {
//             player_input(JUMP);  // Simulate the 'w' key press for jumping
//         } else if (duck_state == HIGH) {
//             player_input(DUCK);  // Simulate the 's' key press for ducking
//         } else if (quit_state == HIGH) {
//             game_over = true;  // Set game over flag to true to end the game
//         }
//     }
// }

// // Function to handle player input and update game actions
// void player_input(Input_State input) {
//     if (!game_over) {
//         game.input(input);
//     }
// }

// void print_compressed_frame(Frame frame) {
// 	// Each column (uint64_t) takes at most 13 characters (16 - 4 for hex, 1
// for comma)
// 	// 1 additional character for '\0'
// 	char buf[MAX_X * 13 + 1] = {0};
// 	frame.compressed_form(buf);
// 	// std::cout << buf << std::endl;
//   Serial.println(buf);
// }

// void setup() {
//     // Initialize serial communication and button pins
//     Serial.begin(115200);
//     // Serial.begin(9600);

//     pinMode(BUTTON_JUMP_PIN, INPUT);  // Set button pins as input
//     pinMode(BUTTON_DUCK_PIN, INPUT);
//     pinMode(BUTTON_QUIT_PIN, INPUT);

//     Serial.println("setup");
// }

// void loop() {
//     // Game game = Game();  // Initialize your game object

//     // Start input thread for button polling
//     std::thread input_thread(input_thread_func);

//     // while (!game.get_collision() && !game_over) {
//     //     // Update the game logic and frame
//     //     game.update_obstacles();
//     //     game.update_frame();
//     //     print_compressed_frame(game.get_frame());
//     //     // print_frame(game.get_frame());  // Print the updated game frame
//     to the Serial Monitor
//     //     delay(SPEED / 1000);  // Add a delay (in milliseconds)
//     // }

//     // Update the game logic and frame
//     game.update_obstacles();
//     game.update_frame();
//     print_compressed_frame(game.get_frame());
//     // print_frame(game.get_frame());  // Print the updated game frame to the
//     Serial Monitor delay(SPEED / 1000);  // Add a delay (in milliseconds)

//     // // Game over
//     // if (game_over) {
//     //     // std::cout << "Game Over!" << std::endl;
//     //     Serial.println("Game Over!");
//     // }

//     // // std::cout << "Score: " << game.get_score() << "\n";
//     // // std::cout << "Press Quit button to quit!\n";
//     // Serial.println("Score");
//     // Serial.println("Quit");

//     // Wait for the quit signal from the button press, while allowing the
//     input thread to finish input_thread.join();

// }