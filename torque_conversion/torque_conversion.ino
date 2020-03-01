float sensorValue = 0;
int counter = 0;
long baudRate = 9600;

void setup(){
    Serial.begin(baudRate);
}

void loop(){
    Serial.print('\n');
    Serial.print(counter);
    Serial.print(sensorValue);
    counter += 1;
    delay(500);
}
