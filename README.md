# Controlling-Arduino-from-Python-GUI
This project is about a python GUI that I developed using Kivy library to control an Arduino UNO.

![image](https://user-images.githubusercontent.com/76060687/119272558-61184580-bbfe-11eb-854a-6f9b6cff14eb.png)

For this project, I have an Arduino uno that controls three leds in three different modes: Blinking mode, Fade mode and Controlled mode for which the leds are controlled by a potentiometer. The arduino has three main variables that I can contorol from the python GUI: Active leds, mode and speed with the possibility to start and stop the process.

In the other part, through the GUI, the user can find available ports, select one, connect/disconnect from it, set configuration (mode, speed ...) and start or stop the process. The GUI displays how many times each led: "was ON" for Blinking mode or "was in maximum brightness" for Fade and Controlled modes. The GUI has a history where every important event is displayed, then saved in a list along with the time it happened. The interface can handle connexion errors if they occure by showing them in the history and in the message box after disconnecting and reseting the counters for each led.

