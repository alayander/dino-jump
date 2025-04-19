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

const int MOTOR_OUTUPUT_PIN = D13;

const int IR_1_THRESHOLD = 300;
const int IR_2_THRESHOLD = 300;
const int SAMPLE_SIZE = 10;

const unsigned long TIMEOUT_LIMIT = 60000;

enum GlobalState { IDLE, READY, RUNNING };

GlobalState global_state = IDLE;
bool prev_foot_detected = false;
bool jump = false;
bool duck = false;

bool state_is_new = true;
unsigned long first_ready_time = 0;

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
  pinMode(MOTOR_OUTUPUT_PIN, OUTPUT);
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
  if (state_is_new) {
    Serial.println("idle");
    state_is_new = false;
  }
  digitalWrite(MOTOR_OUTUPUT_PIN, LOW);

  if (digitalRead(SPIN_BUTTON_PIN) == LOW) {
    digitalWrite(MOTOR_OUTUPUT_PIN, HIGH);
    digitalWrite(DUCK_OUTPUT_PIN, HIGH);
    delay(5);
    digitalWrite(DUCK_OUTPUT_PIN, LOW);

    state_is_new = true;
    global_state = READY;
  }
}

void ready() {
  if (state_is_new) {
    Serial.println("ready");
    first_ready_time = millis();
    state_is_new = false;
  }

  bool timeout = (millis() - first_ready_time) > TIMEOUT_LIMIT ;

  if (timeout) {
    digitalWrite(JUMP_OUTPUT_PIN, HIGH);
    digitalWrite(MOTOR_OUTUPUT_PIN, LOW);
    delay(5);
    digitalWrite(JUMP_OUTPUT_PIN, LOW);
    digitalWrite(MOTOR_OUTUPUT_PIN, HIGH);

    state_is_new = true;
    global_state = IDLE;
  }

  if (digitalRead(START_BUTTON_PIN) == LOW) {
    digitalWrite(DUCK_OUTPUT_PIN, HIGH);
    delay(5);
    digitalWrite(DUCK_OUTPUT_PIN, LOW);

    state_is_new = true;
    global_state = RUNNING;
  }
}

void running() {
  if (state_is_new) {
    Serial.println("running");
    attachInterrupt(digitalPinToInterrupt(DEATH_INPUT_PIN), handle_death, RISING);
    state_is_new = false;
  }
  
  if (digitalRead(SW_PIN) == LOW){
    detect_button_input();
  } else {
    detect_ducking();
    detect_jumping();
  }
}

void handle_death() {
  state_is_new = true;
  global_state = READY;
  detachInterrupt(digitalPinToInterrupt(DEATH_INPUT_PIN));
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
