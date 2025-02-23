const int SAMPLE_SIZE = 10;
const int IR_PIN_1 = A1;
const int IR_PIN_2 = A2;
const int IR_1_THRESHOLD = 500;
const int IR_2_THRESHOLD = 500;

void setup() {
  Serial.begin(9600);  
}

void loop() {
  // print_val();
  print_min_of_samples();
  // detect_ducking();
  delay(5);
}

void print_min_of_samples() {
  int min1 = min_of_samples(IR_PIN_1); 
  char buf[32] = {0};
  sprintf(buf, "1:%d", min1);
  Serial.println(buf);

  if (min1 > IR_1_THRESHOLD) {
    Serial.println("H1");
  } else {
    Serial.println("L1");
  }

  int min2 = min_of_samples(IR_PIN_2); 
  sprintf(buf, "2:%d", min2);
  Serial.println(buf);

  if (min2 > IR_2_THRESHOLD) {
    Serial.println("H2");
  } else {
    Serial.println("L2");
  }
}

void detect_ducking() {
  int min1 = min_of_samples(IR_PIN_1); 
  int min2 = min_of_samples(IR_PIN_2); 

  if (min1 < IR_1_THRESHOLD && min2 < IR_2_THRESHOLD) {
    Serial.println("D");
  }
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
  int read_val = analogRead(IR_PIN_1);
  char buf[32] = {0};
  sprintf(buf, "1:%d", read_val);
  Serial.println(buf);

  read_val = analogRead(IR_PIN_2);
  sprintf(buf, "2:%d", read_val);
  Serial.println(buf);
}
