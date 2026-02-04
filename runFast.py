import GUI

gui = GUI.fastGUI()

isConnected = gui.initGUI()
if(isConnected):
    gui.startGUI()
else:
    print("cannot connect to redpitaya")
    gui.stopGUI()