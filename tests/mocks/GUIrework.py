import sys
from PySide6.QtWidgets import ( QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QStackedWidget, QSlider, QComboBox, QLabel, QLineEdit, QStackedLayout )
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QIntValidator, QDoubleValidator
#test
import pyqtgraph as PGraph
import numpy as np

from mConstants import *

class MenuGUI(QWidget):
    fastBtnCallback = Signal()
    slowBtnCallback = Signal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        fastBtn = QPushButton("Single Run Fast Generator")
        slowBtn = QPushButton("Continuous Generator")

        fastBtn.clicked.connect(self.fastBtnCallback)
        slowBtn.clicked.connect(self.slowBtnCallback)

        fastBtn.setFixedSize(400,80)
        slowBtn.setFixedSize(400,80)

        layout.addWidget(fastBtn)
        layout.addWidget(slowBtn)
        self.setLayout(layout)

class SlowGUI(QWidget):
    # ========== BUTTON CALLBACKS ========== #
    startBtnCallback = Signal()
    stopBtnCallback = Signal()
    resetBtnCallback = Signal()
    pauseBtnCallback = Signal()
    unpauseBtnCallback = Signal()
    flipBtnCallback = Signal()
    saveToCSVBtnCallback = Signal()
    clearPlotBtnCallback = Signal()
    exitBtnCallback = Signal()
    setBtnCallback = Signal()

    # ========== COMBOBOX CALLBACKS ========== #
    genModeCBCallback = Signal()
    directionCBCallback = Signal()
    gainCBCallback = Signal()
    ratioCBCallback = Signal()

    # ========== PLOTTER CALLBACKS ========== #
    plotterCallback = Signal()

    def __init__(self):
        super().__init__()


        # ========== LAYOUTS ========== #
        mainLayout = QGridLayout()
        settingsLayout = QGridLayout() 
        stackerSettingsLayout = QStackedLayout()
        steppingSettingsLayout = QGridLayout()
        normalSettingsLayout = QGridLayout()
        commonSettingsLayout = QGridLayout()
        buttonsLayout = QGridLayout()
        progressLayout = QVBoxLayout()
        plotLayout = QVBoxLayout()
        genPlotLayout = QVBoxLayout()
        errorLayout = QVBoxLayout()

        # ========== BUTTONS ========== #    
        startBtn = QPushButton("START")
        stopBtn = QPushButton("STOP")
        resetBtn = QPushButton("RESET")
        pauseBtn = QPushButton("PAUSE")
        unpauseBtn = QPushButton("UNPAUSE")
        flipBtn = QPushButton("FLIP")
        saveToCSVBtn = QPushButton("SAVE TO CSV")
        clearPlotBtn = QPushButton("CLEAR PLOT")
        exitBtn = QPushButton("EXIT")
        setBtn = QPushButton("SET")

        startBtn.clicked.connect(self.startBtnCallback)
        stopBtn.clicked.connect(self.stopBtnCallback)
        resetBtn.clicked.connect(self.resetBtnCallback)
        pauseBtn.clicked.connect(self.pauseBtnCallback)
        unpauseBtn.clicked.connect(self.unpauseBtnCallback)
        flipBtn.clicked.connect(self.flipBtnCallback)
        saveToCSVBtn.clicked.connect(self.saveToCSVBtnCallback)
        clearPlotBtn.clicked.connect(self.clearPlotBtnCallback)
        exitBtn.clicked.connect(self.exitBtnCallback)
        setBtn.clicked.connect(self.setBtnCallback)

        # ========== ENTRIES ========== # 
        stepEntry = QLineEdit()
        hRangeEntry = QLineEdit()
        lRangeEntry = QLineEdit()
        startPointEntry = QLineEdit()
        maxRangeEntry = QLineEdit()
        numOfStepsEntry = QLineEdit()

        stepEntry.setText(str(GEN_DEFAULT_STEP))
        hRangeEntry.setText(str(GEN_DEFAULT_HRANGE))
        lRangeEntry.setText(str(GEN_DEFAULT_LRANGE))
        startPointEntry.setText(str(GEN_DEFAULT_VOLTAGE))
        maxRangeEntry.setText(str(GEN_DEFAULT_HRANGE))
        numOfStepsEntry.setText(str(GEN_DEFAULT_NUM_STEPS))

        stepEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        hRangeEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        lRangeEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        startPointEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        maxRangeEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        numOfStepsEntry.setValidator(QIntValidator(1,20))

        # ========== COMBOBOXES ========== # 
        genModeCombobox = QComboBox()
        directionCombobox = QComboBox()
        gainCombobox = QComboBox()
        IVRatioCombobox = QComboBox()

        genModeCombobox.addItems(GUI_COMBOBOX_VALUES)
        directionCombobox.addItems(GUI_DIR_COMBOBOX_VALUES)
        gainCombobox.addItems(GUI_GAIN_COMBOBOX_VALUES)
        IVRatioCombobox.addItems(GUI_RATIO_COMBOBOX_VALUES)

        genModeCombobox.setCurrentIndex(0)
        directionCombobox.setCurrentIndex(0)
        gainCombobox.setCurrentIndex(0)
        IVRatioCombobox.setCurrentIndex(0)

        genModeCombobox.currentTextChanged.connect(self.genModeCBCallback)
        directionCombobox.currentTextChanged.connect(self.directionCBCallback)
        gainCombobox.currentTextChanged.connect(self.gainCBCallback)
        IVRatioCombobox.currentTextChanged.connect(self.ratioCBCallback)

        # ========== PROGRESS BAR ========== # 
        progressBar = QSlider()
        progressBar.setTracking(False)
        progressBar.setEnabled(False)
        progressBar.setRange(-1.0, 1.0)

        # ========== PLOTS ========== # 
        acqPlotter = Plotter()
        genPlotter = Plotter()
        #SUBJECT TO CHANGE TODO
        timer = QTimer()
        timer.timeout.connect(self.plotterCallback)
        timer.start(16)

        # ========== LABELS ========== # 
        stepLabel = QLabel("Step value [mV]")
        IVRatioLabel = QLabel("I/V [A/V?]")
        gainLabel = QLabel("Gain mode")
        hRangeLabel = QLabel("High peak value [mV]")
        lRangeLabel = QLabel("Low peak value [mV]")
        startPointLabel = QLabel("Starting value [mV]") #used instead of base label and used for normal
        directionLabel = QLabel("Starting direction")
        maxRangeLabel = QLabel("Limit value [mV]")
        numOfStepsLabel = QLabel("No. of steps")
        errorLabel = QLabel("") #to be filled during program
        progressLabel = QLabel("") #to be filled during program

        # ========== LAYOUT ASSIGNMENT ========== # 
        # mainLayout = QGridLayout()                DONE 
        # settingsLayout = QGridLayout()            DONE 1
        # stackerSettingsLayout = QStackedLayout()  DONE 2
        # steppingSettingsLayout = QGridLayout()    DONE 3
        # normalSettingsLayout = QGridLayout()      DONE 4
        # commonSettingsLayout = QGridLayout()      DONE 5
        # buttonsLayout = QGridLayout()             DONE 6
        # progressLayout = QVBoxLayout()            DONE 7
        # plotLayout = QVBoxLayout()                DONE 8
        # genPlotLayout = QVBoxLayout()             DONE 9
        # errorLayout = QVBoxLayout()               DONE 0


        #     0   1   2   3   4   5   6   7   8   9
        #   ---------------mainLayout----------------
        # 0 | 1 | 1 | . | . | . | 8 | 8 | 8 | 8 | 8 |
        # 1 | 1 | 1 | . | . | . | 8 | 8 | 8 | 8 | 8 |
        # 2 | 1 | 1 | . | . | . | 8 | 8 | 8 | 8 | 8 |
        # 3 | 1 | 1 | . | . | . | 8 | 8 | 8 | 8 | 8 |
        # 4 | 1 | 1 | . | . | . | 8 | 8 | 8 | 8 | 8 |
        # 5 | 7 | 7 | . | . | . | 8 | 8 | 8 | 8 | 8 |
        # 6 | 9 | 9 | 9 | 0 | 0 | 6 | 6 | 6 | 6 | 6 |
        # 7 | 9 | 9 | 9 | 0 | 0 | 6 | 6 | 6 | 6 | 6 |
        # 8 | 9 | 9 | 9 | . | . | . | . | . | . | . |
        # 9 | 9 | 9 | 9 | . | . | . | . | . | . | . |

        
        # GRID SETTINGS --------- .addWidget(xyz, [row], [column], [rowSpan], [columnSpan])

        steppingSettingsLayout.addWidget(maxRangeLabel,     0, 0,   1, 1)
        steppingSettingsLayout.addWidget(maxRangeEntry,     0, 1,   1, 1)
        steppingSettingsLayout.addWidget(numOfStepsLabel,   1, 0,   1, 1)
        steppingSettingsLayout.addWidget(numOfStepsEntry,   1, 1,   1, 1)

        normalSettingsLayout.addWidget(hRangeLabel,         0, 0,   1, 1)
        normalSettingsLayout.addWidget(hRangeEntry,         0, 1,   1, 1)
        normalSettingsLayout.addWidget(lRangeLabel,         1, 0,   1, 1)
        normalSettingsLayout.addWidget(lRangeEntry,         1, 1,   1, 1)
        normalSettingsLayout.addWidget(directionLabel,      2, 0,   1, 1)
        normalSettingsLayout.addWidget(directionCombobox,   2, 1,   1, 1)
        
        #wrapping for stackerSettingsLayout
        steppingSettingsWidgetWrapper = QWidget()
        normalSettingsWidgetWrapper = QWidget()
        steppingSettingsWidgetWrapper.setLayout(steppingSettingsLayout)
        normalSettingsWidgetWrapper.setLayout(normalSettingsLayout)

        stackerSettingsLayout.addWidget(normalSettingsWidgetWrapper) #index 0
        stackerSettingsLayout.addWidget(steppingSettingsWidgetWrapper) #index 1

        commonSettingsLayout.addWidget(startPointLabel, 0, 0,   1, 1)
        commonSettingsLayout.addWidget(startPointEntry, 0, 1,   1, 1)
        commonSettingsLayout.addWidget(stepLabel,       1, 0,   1, 1)
        commonSettingsLayout.addWidget(stepEntry,       1, 1,   1, 1)
        commonSettingsLayout.addWidget(IVRatioLabel,    2, 0,   1, 1)
        commonSettingsLayout.addWidget(IVRatioCombobox, 2, 1,   1, 1)
        commonSettingsLayout.addWidget(gainLabel,       3, 0,   1, 1)
        commonSettingsLayout.addWidget(gainCombobox,    3, 1,   1, 1)
        
        #wrapping for settingsLayout
        stackerSettingsWidgetWrapper = QWidget()
        commonSettingsWidgetWrapper = QWidget()
        stackerSettingsWidgetWrapper.setLayout(stackerSettingsLayout)    
        commonSettingsWidgetWrapper.setLayout(commonSettingsLayout) 

        settingsLayout.addWidget(genModeCombobox,               0, 1,   1, 2)
        settingsLayout.addWidget(stackerSettingsWidgetWrapper,  1, 0,   4, 4)
        settingsLayout.addWidget(commonSettingsWidgetWrapper,   4, 0,   4, 4)
        settingsLayout.addWidget(setBtn,                        8, 1,   1, 2)

        buttonsLayout.addWidget(startBtn,       0, 0,   1, 1)
        buttonsLayout.addWidget(stopBtn,        0, 1,   1, 1)
        buttonsLayout.addWidget(resetBtn,       0, 2,   1, 1)
        buttonsLayout.addWidget(pauseBtn,       1, 0,   1, 1)
        buttonsLayout.addWidget(unpauseBtn,     1, 1,   1, 1)
        buttonsLayout.addWidget(flipBtn,        1, 2,   1, 1)
        buttonsLayout.addWidget(saveToCSVBtn,   2, 0,   1, 1)
        buttonsLayout.addWidget(clearPlotBtn,   2, 1,   1, 1)
        buttonsLayout.addWidget(exitBtn,        2, 2,   1, 1)

        progressLayout.addWidget(progressLabel)
        progressLayout.addWidget(progressBar)

        plotLayout.addWidget(acqPlotter)

        genPlotLayout.addWidget(genPlotter)

        errorLayout.addWidget(errorLabel)

        #wrapping for mainLayout
        settingsWidgetWrapper = QWidget()
        buttonsWidgetWrapper = QWidget()
        progressWidgetWrapper = QWidget()
        plotWidgetWrapper = QWidget()
        genPlotWidgetWrapper = QWidget()
        errorWidgetWrapper = QWidget()
        settingsWidgetWrapper.setLayout(settingsLayout)
        buttonsWidgetWrapper.setLayout(buttonsLayout)
        progressWidgetWrapper.setLayout(progressLayout)
        plotWidgetWrapper.setLayout(plotLayout)
        genPlotWidgetWrapper.setLayout(genPlotLayout)
        errorWidgetWrapper.setLayout(errorLayout)

        mainLayout.addWidget(settingsWidgetWrapper, 0, 0,   5, 2) #1
        mainLayout.addWidget(progressWidgetWrapper, 5, 0,   1, 1)
        mainLayout.addWidget(genPlotWidgetWrapper,  6, 0,   4, 3)
        mainLayout.addWidget(errorWidgetWrapper,    6, 3,   2, 2)
        mainLayout.addWidget(plotWidgetWrapper,     0, 5,   6, 5)
        mainLayout.addWidget(buttonsWidgetWrapper,  6, 5,   2, 5)

        for i in range(9):
            mainLayout.setRowStretch(i, 1)
            mainLayout.setColumnStretch(i, 1)

        self.setLayout(mainLayout)


class FastGUI(QWidget):
    startBtnCallback = Signal()
    exitBtnCallback = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        startBtn = QPushButton("Start")
        exitBtn = QPushButton("EXIT")
        
        exitBtn.clicked.connect(self.exitBtnCallback)

        layout.addWidget(startBtn)
        layout.addWidget(exitBtn)
        self.setLayout(layout)

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.resize(1000,800)

        self.stack = QStackedWidget()

        self.menuGUI = MenuGUI()
        self.slowGUI = SlowGUI()
        self.fastGUI = FastGUI()
    
        self.stack.addWidget(self.menuGUI)
        self.stack.addWidget(self.slowGUI)
        self.stack.addWidget(self.fastGUI)

        # ADD callbacks to the GUIS
        self.menuGUI.fastBtnCallback.connect(self.menu_F_BTN_CBCK)
        self.menuGUI.slowBtnCallback.connect(self.menu_S_BTN_CBCK)


        self.fastGUI.exitBtnCallback.connect(self.fast_exit_BTN_CBCK)


        self.slowGUI.startBtnCallback.connect(self.slow_start_BTN_CBCK)
        self.slowGUI.stopBtnCallback.connect(self.slow_stop_BTN_CBCK)
        self.slowGUI.resetBtnCallback.connect(self.slow_reset_BTN_CBCK)
        self.slowGUI.pauseBtnCallback.connect(self.slow_pause_BTN_CBCK)
        self.slowGUI.unpauseBtnCallback.connect(self.slow_unpause_BTN_CBCK)
        self.slowGUI.flipBtnCallback.connect(self.slow_flip_BTN_CBCK)
        self.slowGUI.saveToCSVBtnCallback.connect(self.slow_saveToCSV_BTN_CBCK)
        self.slowGUI.clearPlotBtnCallback.connect(self.slow_clearPlot_BTN_CBCK)
        self.slowGUI.exitBtnCallback.connect(self.slow_exit_BTN_CBCK)
        self.slowGUI.setBtnCallback.connect(self.slow_set_BTN_CBCK)
        self.slowGUI.genModeCBCallback.connect(self.slow_genMode_CB_CBCK)
        self.slowGUI.directionCBCallback.connect(self.slow_direction_CB_CBCK)
        self.slowGUI.gainCBCallback.connect(self.slow_gain_CB_CBCK)
        self.slowGUI.ratioCBCallback.connect(self.slow_ratio_CB_CBCK)
        self.slowGUI.plotterCallback.connect(self.slow_plotter_CBCK)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

    # ========================= Callbacks ========================= #

    # ============ MENU ============ #
    def menu_F_BTN_CBCK(self):
        #prepare part...
        self.stack.setCurrentIndex(WindowType.FAST)

    def menu_S_BTN_CBCK(self):
        #prepare part...
        self.stack.setCurrentIndex(WindowType.SLOW)

    # ============ FAST GUI ============ #
    def fast_exit_BTN_CBCK(self):
        #logic...
        self.stack.setCurrentIndex(WindowType.MENU)

    # ============ SLOW GUI ============ #
    def slow_start_BTN_CBCK(self):
        #TODO
        pass

    def slow_stop_BTN_CBCK(self):
        #TODO
        pass

    def slow_reset_BTN_CBCK(self):
        #TODO
        pass

    def slow_pause_BTN_CBCK(self):
        #TODO
        pass

    def slow_unpause_BTN_CBCK(self):
        #TODO
        pass

    def slow_flip_BTN_CBCK(self):
        #TODO
        pass

    def slow_saveToCSV_BTN_CBCK(self):
        #TODO
        pass

    def slow_clearPlot_BTN_CBCK(self):
        #TODO
        pass

    def slow_exit_BTN_CBCK(self):
        #TODO
        pass

    def slow_set_BTN_CBCK(self):
        #TODO
        pass

    def slow_genMode_CB_CBCK(self):
        #TODO
        pass

    def slow_direction_CB_CBCK(self):
        #TODO
        pass

    def slow_gain_CB_CBCK(self):
        #TODO
        pass

    def slow_ratio_CB_CBCK(self):
        #TODO
        pass

    def slow_plotter_CBCK(self):
        #TODO
        pass


    # ======================= End Callbacks ======================= #

def run():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

# TEST TO BE PUT IN PLOTTER.PY
class Plotter(PGraph.PlotWidget):
    def __init__(self):
        super().__init__()

        self.setTitle("test")
        self.setYRange(-2,2)

        self.x = np.linspace(0,2*np.pi, 200)
        self.phase = 0
        self.curve = self.plot(self.x, np.sin(self.x), pen="y")

    def updatePlot(self):
        self.phase += 0.1
        y = np.sin(self.x + self.phase)

        self.curve.setData(self.x, y)
