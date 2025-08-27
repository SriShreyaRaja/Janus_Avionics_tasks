int ledGreen = 2;   // Ascending
int ledBlue = 3;    // Apogee
int ledRed = 4;     // Descending
int buzzer = 5;
int forcePin = A0;

int previous = 0;   
bool firstRun = true;  
void setup() {
  pinMode(ledGreen, OUTPUT);
  pinMode(ledBlue, OUTPUT);
  pinMode(ledRed, OUTPUT);
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // taking average of 10 readings (because of errors in measurement )
  int sum = 0;
  for (int i=0; i<10; i++) {
    sum += analogRead(forcePin);
    delay(5);
  }
  int current = sum / 10;

  if (firstRun) {
    previous = current;  
    firstRun = false;
  }


  int threshold = 10;

  if (current < previous - threshold) {
    // Ascending
    digitalWrite(ledGreen, HIGH);
    digitalWrite(ledBlue, LOW);
    digitalWrite(ledRed, LOW);
    noTone(buzzer);
  }
  else if (current > previous + threshold) {
    // Descending
    digitalWrite(ledGreen, LOW);
    digitalWrite(ledBlue, LOW);
    digitalWrite(ledRed, HIGH);
    noTone(buzzer);
  }
  else {
    // Apogee
    digitalWrite(ledGreen, LOW);
    digitalWrite(ledBlue, HIGH);
    digitalWrite(ledRed, LOW);

    // Only buzz once when apogee is reached
    tone(buzzer, 1000);
    delay(200);
    noTone(buzzer);
  }

  previous = current;  // update
  delay(200);
}