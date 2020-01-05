void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  delay(500);
  Serial.println("Firmware Version: 0x88 = (clone)");
  Serial.println("Scan PICC to see UID, SAK, type, and data blocks...");
}

String serialread;

void readport(){
  if (Serial.available()){
    //delay(100);
    serialread = Serial.readString();
    if (serialread == "1"){
      digitalWrite(13, HIGH);
      delay(10000);
      digitalWrite(13, LOW);
      serialread == "";
      delay(1000);
    }
    else if (serialread == "2"){
      digitalWrite(13, HIGH);
      delay(400);
      digitalWrite(13, LOW);
      delay(400);
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(13, LOW);
      serialread == "";
    }
    else if (serialread == "3"){
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(13, LOW);
      delay(200);
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(13, LOW);
      delay(200);
      digitalWrite(13, HIGH);
      delay(200);
      digitalWrite(13, LOW);
      serialread == "";
    }
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  int r = random(1,5);
  switch (r){
    case 1:
      Serial.println("-Arduino Card UID: F3 7B 42 1B");
      Serial.println("Sector Block   0  1  2  3   4  5  6  7   8  9 10 11  12 13 14 15  AccessBits");
      break;
    case 2:
      Serial.println("-Arduino Card UID: F7 7B 42 1B");
      Serial.println("Sector Block   0  1  2  3   4  5  6  7   8  9 10 11  12 13 14 15  AccessBits");
      break;
    case 3:
      Serial.println("-Arduino Card UID: B2 7B 42 1B");
      Serial.println("Sector Block   0  1  2  3   4  5  6  7   8  9 10 11  12 13 14 15  AccessBits");
      break;
    case 4:
      Serial.println("-Arduino Card UID: CC CC CC CC");
      Serial.println("Sector Block   0  1  2  3   4  5  6  7   8  9 10 11  12 13 14 15  AccessBits");
      break;
  }
  for (int i = 0; i < 20; i++){
    readport();
    delay(500);
  }
}
