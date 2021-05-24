In this repository you will find:
- interface.py (python GUI code)
- syle.kv (kivy language file for GUI styling)
- interface.ino (arduino c++ code)

By uploading interface.ino to arduino using arduino IDE where you should install TimerOne library (https://github.com/PaulStoffregen/TimerOne) and running interface.py using an interpreter that has kivy library installed, you should be able to control the arduino from the GUI through USB serial communication.

  The arduino and the interface communicate through usb cable (UART) under a protocol of communication, a request is sent under the form ($x-x-x-x&) where $ is a symbole that indicates the type of information that is sent, and based on it the arduino parse some specefied varibales to be changed. Until now I have only two symboles: "$" for configuration (changing speed, mode and active leds) and "*" for start and stop (changing processStarted variable). Each x represents an integer to be parsed and finally "&" indicates the end of the message. For example: $1-0-1-2-7& will be parsed as (activeLeds[] = {1, 0, 1}, mode = 2, speed = 7), *0& sets the processStarted varialbe to false and *1& does the oposite.
  
  The arduino gives feedback to the interface under the form $x-x-x& where each x represents the number of times a led was on maximum brightness (255). There is also another type of messges that are used for establishing connection: In the setup() function, the arduino keeps infinitely writing "C" to Serial every second until it gets another "C" as a response from the GUI, then it sends "C1" to the GUI and goes to the loop() function.
  
  The code for controlling leds is easy, it has three modes, each mode is written inside an if(mode=x) statement where mode variable can take 1 for blinking, 2 for fading or 3 for controlled mode as values. But before the modes we have two important blocks, the flag block under if(flag) to be executed whenever there is a new message and an empty while(!processStarted && !flag) that does nothing but stop the process unless the process is started (processStarted=true) or there is a flag to change variables or to start the process.
  
  Reading serial data and controlling leds at the same time is possible thanks to TimerOne library which allows us to execute a function repeatedly, I used it to read one character from Serial and concatenate it to Request variable which holds the $-x-x-...-x& request. This function ignores "C" characters that may be sent to establish connexion at the beginning and to set the flag to true when it reads a & varibale. So that the next time the loop starts the flag block will be executed. The later stops TimerOne from reading to request varibale so that it can, depending on the first character (& or *), parse the right variables. Fianlly the flag is set to false after restarting TimerOne.
  
Note: TimerOne library uses digital pins 9 and 10 so you can't use them.
  
  The interface also reads from serial each 100 ms and takes a decision: sending "C" for connexion establishing, showing that connextion has been established when receiving "C1" and updating counters when receiving $x-x-x&. It also sends start/stop and configuration requests.
