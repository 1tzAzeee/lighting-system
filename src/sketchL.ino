const int s0 = 2;
const int s1 = 3;
const int s2 = 4;
const int sig = 7;



void setup() {
  Serial.begin(9600);
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(sig, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){
    String msg = Serial.readString();

    handler(msg);
  }
}

void channelSelect(int channel){
  digitalWrite(s0, bitRead(channel, 0));
  digitalWrite(s1, bitRead(channel, 1));
  digitalWrite(s2, bitRead(channel, 2));
}

void handler(String message){
  int spaceIndex = message.indexOf(' ');
  Serial.print(message);
  if (spaceIndex != -1) {
    String command = message.substring(0, spaceIndex);
    String numberStr = message.substring(spaceIndex + 1);
    int number = numberStr.toInt();
    
    channelSelect(number);
    if (command == "on"){
      digitalWrite(sig, HIGH);
    }
    else{
      digitalWrite(sig, LOW);
    }
  }
}





