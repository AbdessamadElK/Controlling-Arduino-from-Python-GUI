# Controlling-Arduino-from-Python-GUI
This project is about a python GUI that I developed using Kivy library to control an Arduino UNO.

For this project, I have an Arduino uno that controls three leds in three different modes: Blinking mode, Fade mode and Controlled mode ( the leds are controlled by a potentiometer). The arduino has three main variables that I can contorol from the python GUI: Active leds, mode and speed. I can also start and stop the process.

In the other part, the python GUI can find available ports, select one, connect/disconnect from it, set configuration (mode, speed ...), start/stop and it shows how many times a each led was ON for Blinking mode, in maximum brightness for Fade and Controlled modes. The GUI has a history where every important event is deplayed and saved in a list along with the time it happened to be exported later (I still didn't make this part). The interface can handle connexion errors if they occure by showing them in the history and in a message box after disconnecting and reseting the counters for each led.

The final part of the project if to be able to export the history and to make a PDF report about the operation in form of graphs (for example a histogram comparing led counters).

🚨 IMPORTANT NOTES:
- This is my first GUI, actually my first "Upload to github worthy" project. So the code may be messy.
- This is but a test project, I made this project as a preparation for a bigger project: "Controlling a Color Sorting Machine from python GUI"

