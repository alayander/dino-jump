const int DUCK_INPUT_PIN_1 = A1;
const int DUCK_INPUT_PIN_2 = A2;
const int DUCK_OUTPUT_PIN = D0;
const int JUMP_OUTPUT_PIN = D1;
const int JUMP_INPUT_BEAM_PIN = D2;
const int SW_PIN = D3;
const int BUTTON_DUCK_INPUT_PIN = D4;
const int BUTTON_JUMP_INPUT_PIN = D5;

const int IR_1_THRESHOLD = 500;
const int IR_2_THRESHOLD = 500;
const int SAMPLE_SIZE = 10;

bool prev_foot_detected = false;
bool jump = false;
bool duck = false;

void setup() {
  Serial.begin(9600);
  pinMode(DUCK_OUTPUT_PIN, OUTPUT);
  pinMode(JUMP_OUTPUT_PIN, OUTPUT);
  pinMode(JUMP_INPUT_BEAM_PIN, INPUT_PULLUP);
  pinMode(SW_PIN, INPUT_PULLUP);
  pinMode(BUTTON_DUCK_INPUT_PIN, INPUT_PULLUP);
  pinMode(BUTTON_JUMP_INPUT_PIN, INPUT_PULLUP);
}

void loop() {
  if(digitalRead(SW_PIN) == LOW){
    detect_button_input();
  } else {
    detect_ducking();
    detect_jumping();
  }

  delay(5);
}

void detect_button_input(){
  duck = digitalRead(BUTTON_DUCK_INPUT_PIN) == LOW;

  digitalWrite(DUCK_OUTPUT_PIN, duck);
  Serial.print("Duck: ");
  Serial.println(duck);

  jump = digitalRead(BUTTON_JUMP_INPUT_PIN) == LOW;

  digitalWrite(JUMP_OUTPUT_PIN, jump);
  Serial.print("Jump: ");
  Serial.println(jump);

}

void print_min_of_samples() {
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
  Serial.print("Duck: ");
  Serial.println(duck);
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
  bool foot_detected = digitalRead(JUMP_INPUT_BEAM_PIN) == LOW;
  bool jump = prev_foot_detected && !foot_detected;
  if (jump) {
    Serial.println("J");
  }
  prev_foot_detected = foot_detected;

  digitalWrite(JUMP_OUTPUT_PIN, jump);
  Serial.print("Jump: ");
  Serial.println(jump);

}