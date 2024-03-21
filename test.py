from appJar import gui

def press(button):
    if button == "Cancel":
        appGui.stop()
    else:
        print(appGui.getEntry("Test"))

appGui = gui("TEST", "1000x1000")

appGui.addLabel("title", "SIEMA ENIU :D") #po prostu tekst
appGui.setLabelBg("title", "blue") #background
appGui.addLabel("Amplituda", "amplituda")
appGui.addNumericEntry("Amplituda")
appGui.addNumericEntry("Czestotliwosc")
appGui.addNumericEntry("Kanal")
appGui.addButton("Essa", press) #dodaje przycisk na ekranie
appGui.bindKey("<Return>", press) #dodaje przycisk na klawie do obslugi



appGui.go()