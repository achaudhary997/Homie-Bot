int motorPin = 3;

void setup() {
  pinMode(motorPin, OUTPUT);
  
}

void loop() {
 
    unsigned int uS = sonar.ping();
    float dist=uS/US_ROUNDTRIP_CM;
    if(dist<15 && dist>=1)
    {
      analogWrite(motorPin, 0);
    }
    else
    {
      analogWrite(motorPin, 50);
    }
  }

