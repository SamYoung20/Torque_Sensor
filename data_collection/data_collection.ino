int analogPin = A0;
float sensorValue = 0;
long baudRate = 9600;

void setup(){
    Serial.begin(baudRate);
}


void loop(){
    Serial.print('\n');
    sensorValue = analogRead(analogPin);
    Serial.print(sensorValue);
    delay(500);
}
