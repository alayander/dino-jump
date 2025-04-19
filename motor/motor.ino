#include "DualVNH5019MotorShield.h"

DualVNH5019MotorShield md;

#define START_PIN A5
#define ANALOG_THRESHOLD 250

bool spin = false;

void setup()
{
  pinMode(START_PIN, INPUT);
  
  md.init();

  Serial.begin(9600);
}

void loop()
{
  if (digitalRead(START_PIN) == HIGH) {
    md.setM1Speed(129);
  } else {
    md.setM1Speed(0);
  }
}
