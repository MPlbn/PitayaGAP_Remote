from appJar import *
import ttkthemes


# app = gui("TEST", "500x500", useTtk=True)

# app.setTtkTheme("breeze")

# with app.labelFrame("testlabelFrame"):
#     app.label("test1", 'testowy1',  0 ,0, sticky='w', stretch='none')
#     app.entry("testentry1", row=0, column=1, stretch='none', width='15')
#     app.label("test2", 'testowy2',  1 ,0, sticky='w', stretch='none')
#     app.entry("testentry2", row=1, column=1, stretch='none', width='15')
#     app.label("test3", 'testowy3',  2 ,0, sticky='w', stretch='none')
#     app.entry("testentry3", row=2, column=1, stretch='none', width='15')

# with app.frame("testframe2"):
#     app.button("testb1", row=0, column=0)
#     app.button("testb2", row=1, column=0)
#     app.button("testb3", row=2, column=0)



# app.go()
app=gui("Grid Demo", "300x300")
app.setSticky("news")
app.setExpand("both")
app.setFont(20)
with app.labelFrame("testlabel", 0 ,0, colspan = 3):
    app.label("l1", "1", 0, 0, sticky='news')
    app.label("l2", "2", 0, 2, sticky='news')
    app.label("l3", "3", 0, 3, sticky='ew')
app.addLabel("l4", "4", 1, 0)
app.addLabel("l5", "5", 1, 1)
app.addLabel("l6", "6", 1, 2)
app.addLabel("l7", "7", 2, 0)
app.addLabel("l8", "8", 2, 1)
app.addLabel("l9", "9", 2, 2)

app.setLabelBg("l1", "LightYellow")
app.setLabelBg("l2", "LemonChiffon")
app.setLabelBg("l3", "LightGoldenRodYellow")
app.setLabelBg("l4", "PapayaWhip")
app.setLabelBg("l5", "Moccasin")
app.setLabelBg("l6", "PeachPuff")
app.setLabelBg("l7", "PaleGoldenRod")
app.setLabelBg("l8", "Khaki")
app.setLabelBg("l9", "DarkKhaki")

app.go()