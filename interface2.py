from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.clock import Clock
from kivy.lang.builder import Builder

from chaineCommunication import myArduino
from time import sleep
from datetime import datetime
from serial.serialutil import SerialException, Timeout
from serial.tools.list_ports_windows import comports


Builder.load_file("style.kv")

class mainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(mainLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
    #connextion variables:
        self.uno = None
        self.port = "COM6"
        self.connected = False

    #configuration variables:
        self.mode = 1
        self.speed = 4
        self.leds = [True, False, False]
        self.started = False

    #history variables
        self.history = []
        self.hist = self.ids.History
        self.hist.data = []

    #information vatiables
        self.counters = [self.ids.redCounter, self.ids.greenCounter, self.ids.blueCounter]
        self.counts = [0, 0, 0]
    def getTime(self, date = False):
        now = datetime.now()
        if(date):
            return now
        else:
            return now.strftime("%H:%M:%S")


    def setPort(self, value):
        self.port = value
    
    def setMode(self, value):
        if value == "Blink":
            self.mode = 1
        elif value == "Fade":
            self.mode = 2
        elif value == "Controlled":
            self.mode = 3

    def switchLed(self, index):
        self.leds[index] = not self.leds[index]


    def setSpeed(self, value):
        self.speed =  value
        self.ids.speedLabel.text = f"Speed: {value}"


    def initialState(self):
        self.uno = None
        self.connected = False
        self.started = False

        self.ids.startButton.background_color = (.1, .8, .1, 1)
        self.ids.startButton.text = "Start"
        self.ids.startButton.disabled = True

        self.ids.connectButton.background_color = (.1, .1, .8, 1)
        self.ids.connectButton.text = "Connect"

        self.ids.mode.text = "Blink"
        self.ids.speedLabel.text = "Speed: 4"
        self.ids.speedSlider.value = 4
        self.ids.redSwitch.active = True
        self.ids.greenSwitch.active = False
        self.ids.blueSwitch.active = False
        self.ids.updateButton.disabled = True

        for counter in self.counters:
            counter.text = '0'

        for count in self.counts:
            count = 0


    def connectPort(self, connectButton):
        try:
            if not self.connected:
                    self.uno = myArduino(self.port, 9600, timeout = .1)
                    self.updateHistory(f"Connected to {self.port}")
                    self.connected = True

                    connectButton.background_color = (.8, .1, .1, 1)
                    connectButton.text = 'Disconnect'
                    self.showMessage(f"Connected to {self.port}", "Success")     
            else:
                self.uno.start(False)
                self.initialState()
                self.updateHistory(f"Disconnected from {self.port}")
                self.showMessage(f"Disconnected from {self.port}", "Neutral")
        
        except (SerialException, AttributeError):
                self.handleConnexionError()
        
    
    def start(self, startButton):
        if(not self.started):
            try:
                self.uno.start(True)
                self.started = True
                startButton.background_color = (.8, .1, .1, 1)
                startButton.text = "stop"
                self.updateHistory("Process started")
                self.showMessage("Process started", "Neutral")
            except (SerialException, AttributeError):
                self.handleConnexionError()

        else:
            try:
                self.uno.start(False)
                startButton.background_color = (.1, .8, .1, 1)
                self.started = False                
                startButton.text = "Start"
                self.updateHistory("Process stopped")
                self.showMessage("Process stopped", "Neutral")
            except (SerialException, AttributeError):
                self.handleConnexionError()


    def update(self):
        if(self.connected):
            try:
                self.uno.configure([int(x) for x in self.leds], self.mode, self.speed)
                for i in range(3):
                    self.counters[i].background_color[-1] = .5 + .5 * self.leds[i]
                self.updateHistory(f"Update ${int(self.leds[0])}-{int(self.leds[1])}-{int(self.leds[2])}-{self.mode}-{self.speed}&")
                self.showMessage("Updated configuration", "Success")
            except (SerialException, AttributeError):
                self.handleConnexionError()


    def updateHistory(self, title):
        time = self.getTime()
        label = time + "  ---  " + title
        self.hist.data.append({"text": label})
        self.hist.refresh_from_data()
        self.history.append((time, title))
    

    def showMessage(self, msg, msgType):
        msgBox = self.ids.msgBox
        msgBox.text = msg
        if(msgType == "Success"):
            color = (.1, .8, .1, 1)
        elif(msgType == "Fail"):
            color = (.8, .1, .1, 1)
        elif(msgType == "Neutral"):
            color = (0, 0, 0, 1)
        self.ids.msgHolder.background_color = color


    def showCount(self, counts):
        self.counts = counts
        for i in range(3):
            self.counters[i].text = str(self.counts[i])


    def handleConnexionError(self):
        self.updateHistory("Connexion Error!")
        self.showMessage("Connexion Error!", "Fail")
        self.initialState()



class interface(App):
    def build(self):
        Config.set('graphics', 'minimum_width', '940')
        Config.set('graphics', 'minimum_height', '600')
        Config.set('graphics', 'width', '940')
        Config.set('graphics', 'height', '600')
        Config.set('graphics', 'resizable', 'False')
        self.layout = mainLayout()
        availablePorts = comports()
        for port in availablePorts:
            self.layout.ids.ports.values.append(port.device)

        Clock.schedule_interval(self.Respond, 0.1)

        return self.layout

    def Respond(self, *args):
        try:
            data = self.layout.uno.receive()
            if data:
                if data == "C":
                    self.layout.uno.send("C")
                if data == "C1":
                    self.layout.updateHistory("Connexion Established")
                    self.layout.uno.configure([int(x) for x in self.layout.leds], self.layout.mode, self.layout.speed)
                    self.layout.updateHistory(f"Sent Configuration ${int(self.layout.leds[0])}-{int(self.layout.leds[1])}-{int(self.layout.leds[2])}-{self.layout.mode}-{self.layout.speed}&")
                    self.layout.ids.startButton.disabled = False
                    self.layout.ids.updateButton.disabled = False

                if data[0] == '$' and data[-1] == '&':
                    counts = data[1:-1].split('-')
                    self.layout.showCount(counts)
                    self.layout.updateHistory(f"Received : {data}")
        except (SerialException, AttributeError):
                if(self.layout.connected):
                    self.layout.handleConnexionError()
                else:
                    pass

if __name__ == "__main__":
    interface().run()