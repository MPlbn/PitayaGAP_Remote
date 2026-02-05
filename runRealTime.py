#custom modules
import GUI

#creating GUI
gui = GUI.GUI()

#starting GUI and work routines
isConnected = gui.initGUI()
if(isConnected):
    gui.startGUI()
else:
    print("cannot connect to redpitaya")
    gui.stopGUI()

