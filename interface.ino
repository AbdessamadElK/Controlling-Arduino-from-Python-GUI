#include <TimerOne.h>

#define red 3
#define green 5
#define yellow 6

// Program variables:
  const int leds[3] {red, green, yellow};
  int counters[3] {0, 0, 0};
  bool activeLeds[3] {true, false, false};
  volatile int mode = 1;
  int wait = 1000;

  int fadeAmount = 5;
  int brightness = 0;
  int fadeDelay = 30;

  int ptmValue;

// Communication variables:
  volatile bool flag = true;
  char request[15] = "";
  char ledResponse[50] = "";
  volatile int spd = 4;
  volatile bool startProcess = false;
  
  
void setup() {
  for(int led: leds){
    pinMode(led, OUTPUT);
  }
  Timer1.initialize(1000);
  Timer1.attachInterrupt(getConfiguration);
  Serial.begin(9600);

  while(!Serial){
    ;
  }
  
  Timer1.stop();
  char c;
  while(true){
    Serial.println("C");
    delay(1000);
    c = Serial.read();
    if(c == 'C'){
      Serial.println("C1");
      break;
    } 
  }
  Timer1.restart();
}

void loop() {
// flag:
startPoint:
  if(flag){
    Timer1.stop();
    for(int led: leds){
      digitalWrite(led, LOW);
    }
    if(request[0] == '$'){
      sscanf(request, "$%d-%d-%d-%d-%d&", &activeLeds[0], &activeLeds[1], &activeLeds[2], &mode, &spd);
    }else if(request[0] == '*'){
      sscanf(request, "*%d&", &startProcess);
    }
    request[0] = '\0';
    Timer1.restart(); 
    wait = 2000/spd;
    flag = false;
    
  }

  while(!startProcess && !flag){
    delay(100);
  }

//mode 1:
  if(flag) goto startPoint;
  if(mode == 1){
    ledsBlink(HIGH);
    plusCount();
    delay(wait/2);
    ledsBlink(LOW);
    delay(wait/2);
  }

//mode 2:
  if(flag) goto startPoint;
  if(mode == 2){
    ledsFade(brightness);
    brightness += fadeAmount;
    if(brightness >= 255 || brightness <=0){
      if(brightness){
        plusCount();
      }
      fadeAmount = -fadeAmount;
    }
    delay((int)wait/10);
  }

  if(flag) goto startPoint;
  if(mode == 3){
    ptmValue = analogRead(A0);
    ptmValue = map(ptmValue, 0, 1023, 0, 255);
    if(ptmValue >= 255){
      plusCount();
      delay(1000);
    }
    ledsFade(ptmValue);
    delay(10);
  } 
}

// program functions:
void ledsBlink(bool state){
  for(int i = 0; i < 3; i++){
    if(activeLeds[i]){
      digitalWrite(leds[i], state);
    }
  }
}

void ledsFade(int value){
  for(int i = 0; i < 3; i++){
    if(activeLeds[i]){
      analogWrite(leds[i], value);
    }
  }
}

void plusCount(){
  Timer1.stop();
  for(int i = 0; i < 3; i++){
    if (activeLeds[i]) ++counters[i];
  }
  sprintf(ledResponse, "$%d-%d-%d&", counters[0], counters[1], counters[2]);
  Serial.println(ledResponse);
  Timer1.restart();
}


//Communication functions:

void getConfiguration(){
  if(Serial.available() > 0){
    char c[2];
    c[0] = Serial.read();
    c[1] = '\0';
    
    if(c[0]=='C'){
      return;
    }
    
    strcat(request, c);
    if(c[0] == '&'){
      flag = true;
    }
  }
}
