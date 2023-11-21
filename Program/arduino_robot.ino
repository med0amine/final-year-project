const int LIGHT_SENSOR_PIN = A0;
const int LED_PIN          = 13;
const int ANALOG_THRESHOLD = 20;
const int trigPin          = 9;
const int echoPin          = 10;
const int trigPin1         = 11;
const int echoPin1         = 12;

int analogValue;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);
  pinMode(trigPin1, OUTPUT); 
  pinMode(echoPin1, INPUT);
  Serial.begin(9600); 
}
void loop() {
  led();
  long distanceLeft = calcDistance(echoPin, trigPin);
  long distanceRight = calcDistance(echoPin1, trigPin1);
  if (distanceLeft < 25)
     Serial.write(1);
  else if (distanceRight < 25)
     Serial.write(2);
}
void led(){
  analogValue = analogRead(LIGHT_SENSOR_PIN);

  if (analogValue < ANALOG_THRESHOLD)
     digitalWrite(LED_PIN, HIGH);
  else
     digitalWrite(LED_PIN, LOW);
}
long calcDistance(int echo, int trigger){
    long distance = 5000; //number that's bigger than the distance can be
    
    for (int i = 0; i <= 1; i++) {
      long responseTime, responseDistance;
      
      digitalWrite(trigger, LOW);
      delayMicroseconds(2);
      digitalWrite(trigger, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigger, LOW);
 
      responseTime = pulseIn(echo, HIGH);
    
      responseDistance = responseTime / 29 / 2;
      
      if(distance > responseDistance ){
        distance = responseDistance;
      }
    }
    return distance;
}