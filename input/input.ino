const int DUCK_INPUT_PIN_1 = A1;
const int DUCK_INPUT_PIN_2 = A2;

const int DUCK_OUTPUT_PIN = D11;
const int JUMP_OUTPUT_PIN = D12;

const int JUMP_INPUT_BEAM_PIN_1 = D6; 
const int JUMP_INPUT_BEAM_PIN_2 = D7;
const int JUMP_INPUT_BEAM_PIN_3 = D8;

const int SW_PIN = D3;
const int DUCK_BUTTON_INPUT_PIN = D4;
const int JUMP_BUTTON_INPUT_PIN = D5;

const int SPIN_BUTTON_PIN = D9;
const int START_BUTTON_PIN = D10;

const int DEATH_INPUT_PIN = D2;

const int MOTOR_OUTPUT_PIN = D13;

const int IR_1_THRESHOLD = 300;
const int IR_2_THRESHOLD = 300;
const int SAMPLE_SIZE = 10;

const unsigned long TIMEOUT_LIMIT = 60000;

enum GlobalState { IDLE, READY, RUNNING };

GlobalState global_state = IDLE;
bool prev_foot_detected = false;
bool jump = false;
bool duck = false;

void setup() {
  Serial.begin(9600);

  pinMode(DUCK_OUTPUT_PIN, OUTPUT);
  pinMode(JUMP_OUTPUT_PIN, OUTPUT);

  pinMode(JUMP_INPUT_BEAM_PIN_1, INPUT_PULLUP);
  pinMode(JUMP_INPUT_BEAM_PIN_2, INPUT_PULLUP);
  pinMode(JUMP_INPUT_BEAM_PIN_3, INPUT_PULLUP);

  pinMode(SW_PIN, INPUT_PULLUP);
  pinMode(DUCK_BUTTON_INPUT_PIN, INPUT_PULLUP);
  pinMode(JUMP_BUTTON_INPUT_PIN, INPUT_PULLUP);

  pinMode(SPIN_BUTTON_PIN, INPUT_PULLUP);
  pinMode(START_BUTTON_PIN, INPUT_PULLUP);

  pinMode(DEATH_INPUT_PIN, INPUT);
  pinMode(MOTOR_OUTPUT_PIN, OUTPUT);
}

void loop() {
  switch (global_state) {
    case IDLE:
      idle();
      break;

    case READY:
      ready();
      break;

    case RUNNING:
      running();
      break;

    default:
      break;
  }

  delay(1);
}

void idle() {
  Serial.println("idle");
  digitalWrite(MOTOR_OUTPUT_PIN, LOW);

  while (digitalRead(SPIN_BUTTON_PIN) != LOW);
  
  digitalWrite(MOTOR_OUTPUT_PIN, HIGH);
  digitalWrite(DUCK_OUTPUT_PIN, HIGH);
  delay(5);
  digitalWrite(DUCK_OUTPUT_PIN, LOW);

  global_state = READY;
}

void ready() {
  Serial.println("ready");
  unsigned long first_ready_time = millis();

  bool start = false;
  bool timeout = (millis() - first_ready_time) > TIMEOUT_LIMIT;
  while (!timeout && !start) {
    timeout = (millis() - first_ready_time) > TIMEOUT_LIMIT;
    start = digitalRead(START_BUTTON_PIN) == LOW;
  }
  
  if (timeout) {
    digitalWrite(JUMP_OUTPUT_PIN, HIGH);
    digitalWrite(MOTOR_OUTPUT_PIN, LOW);
    delay(5);
    digitalWrite(JUMP_OUTPUT_PIN, LOW);
    digitalWrite(MOTOR_OUTPUT_PIN, HIGH);

    global_state = IDLE;
  }

  if (start) {
    digitalWrite(DUCK_OUTPUT_PIN, HIGH);
    delay(5);
    digitalWrite(DUCK_OUTPUT_PIN, LOW);

    global_state = RUNNING;
  }
}

// TODO Registering death unexpectedly
void running() {
  Serial.println("running");
  attachInterrupt(digitalPinToInterrupt(DEATH_INPUT_PIN), handle_death, RISING);

  while (global_state == RUNNING) {
    if (digitalRead(SW_PIN) == LOW){
      detect_button_input();
    } else {
      detect_ducking();
      detect_jumping();
    }
  }

  digitalWrite(DUCK_OUTPUT_PIN, LOW);
  digitalWrite(JUMP_OUTPUT_PIN, LOW);
  detachInterrupt(digitalPinToInterrupt(DEATH_INPUT_PIN));
}

void handle_death() {
  global_state = READY;
}

void detect_button_input(){
  duck = digitalRead(DUCK_BUTTON_INPUT_PIN) == LOW;

  digitalWrite(DUCK_OUTPUT_PIN, duck);
  Serial.print("Duck: ");
  Serial.println(duck);

  jump = digitalRead(JUMP_BUTTON_INPUT_PIN) == LOW;

  digitalWrite(JUMP_OUTPUT_PIN, jump);
  Serial.print("Jump: ");
  Serial.println(jump);

}

void print_min_of_samples() {
  char buf[32] = {0};
  int min1 = min_of_samples(DUCK_INPUT_PIN_1); 
  sprintf(buf, "1:%d", min1);
  Serial.println(buf);

  if (min1 > IR_1_THRESHOLD) {
    Serial.println("H1");
  } else {
    Serial.println("L1");
  }

  int min2 = min_of_samples(DUCK_INPUT_PIN_2); 
  sprintf(buf, "2:%d", min2);
  Serial.println(buf);

  if (min2 > IR_2_THRESHOLD) {
    Serial.println("H2");
  } else {
    Serial.println("L2");
  }
}

void detect_ducking() {
  int min1 = min_of_samples(DUCK_INPUT_PIN_1); 
  int min2 = min_of_samples(DUCK_INPUT_PIN_2); 

  duck = min1 < IR_1_THRESHOLD && min2 < IR_2_THRESHOLD;
  if (duck) {
    Serial.println("D");
  }
  
  digitalWrite(DUCK_OUTPUT_PIN, duck);
  //Serial.print("Duck: ");
  //Serial.println(duck);
}

int min_of_samples(const int pin) {
  uint32_t min = 0xFFFFFFFF; 

  for (int i = 0; i < SAMPLE_SIZE; i++) {
    int val = analogRead(pin);
    if (min > val) {
      min = val;
    }
  }

  return min;
}


void print_val() {
  // analogRead takes ~100us
  int read_val = analogRead(DUCK_INPUT_PIN_1);
  char buf[32] = {0};
  sprintf(buf, "1:%d", read_val);
  Serial.println(buf);

  read_val = analogRead(DUCK_INPUT_PIN_2);
  sprintf(buf, "2:%d", read_val);
  Serial.println(buf);
}

void detect_jumping() {
  bool foot_detected = digitalRead(JUMP_INPUT_BEAM_PIN_1) == LOW
                    || digitalRead(JUMP_INPUT_BEAM_PIN_2) == LOW
                    || digitalRead(JUMP_INPUT_BEAM_PIN_3) == LOW;
                    //if any pair of beam sensors detect a foot -> one of them low (== eval to 1) -> makes everything true -> foot detected
                    //if any pair of beam sensors detect NO foot -> one of them high (== eval to 0) -> everything false only if all of them false -> no foot detected
   // Serial.print("PIN 1");
   // Serial.println(digitalRead(JUMP_INPUT_BEAM_PIN_1));
   // Serial.print("PIN 2");
   // Serial.println(digitalRead(JUMP_INPUT_BEAM_PIN_2));
   // Serial.print("PIN 3");
   // Serial.println(digitalRead(JUMP_INPUT_BEAM_PIN_3));
  bool jump = prev_foot_detected && !foot_detected;
  if (jump) {
    Serial.println("J");
  }
  prev_foot_detected = foot_detected;

  digitalWrite(JUMP_OUTPUT_PIN, jump);
  //Serial.print("Jump: ");
  //Serial.println(jump);

}
