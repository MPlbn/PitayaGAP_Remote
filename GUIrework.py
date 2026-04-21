import sys
from PySide6.QtWidgets import ( QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QStackedWidget, QProgressBar, QComboBox, QLabel, QLineEdit, QStackedLayout )
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QIntValidator, QDoubleValidator
#test\
import time
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

    # ========== PLOTTER CALLBACKS =========== #
    plotterCallback = Signal()

    def __init__(self):
        super().__init__()


        # ========== LAYOUTS ========== #
        self.mainLayout = QGridLayout()
        self.settingsLayout = QGridLayout() 
        self.stackerSettingsLayout = QStackedLayout()
        self.steppingSettingsLayout = QGridLayout()
        self.normalSettingsLayout = QGridLayout()
        self.commonSettingsLayout = QGridLayout()
        self.buttonsLayout = QGridLayout()
        self.progressLayout = QVBoxLayout()
        self.plotLayout = QVBoxLayout()
        self.genPlotLayout = QVBoxLayout()
        self.errorLayout = QVBoxLayout()

        # ========== BUTTONS ========== #    
        self.startBtn = QPushButton("START")
        self.stopBtn = QPushButton("STOP")
        self.resetBtn = QPushButton("RESET")
        self.pauseBtn = QPushButton("PAUSE")
        self.unpauseBtn = QPushButton("UNPAUSE")
        self.flipBtn = QPushButton("FLIP")
        self.saveToCSVBtn = QPushButton("SAVE TO CSV")
        self.clearPlotBtn = QPushButton("CLEAR PLOT")
        self.exitBtn = QPushButton("EXIT")
        self.setBtn = QPushButton("SET")

        self.startBtn.setObjectName("green")
        self.stopBtn.setObjectName("red")
        self.exitBtn.setObjectName("red")
        self.setBtn.setObjectName("smallClassic")

        self.startBtn.clicked.connect(self.startBtnCallback)
        self.stopBtn.clicked.connect(self.stopBtnCallback)
        self.resetBtn.clicked.connect(self.resetBtnCallback)
        self.pauseBtn.clicked.connect(self.pauseBtnCallback)
        self.unpauseBtn.clicked.connect(self.unpauseBtnCallback)
        self.flipBtn.clicked.connect(self.flipBtnCallback)
        self.saveToCSVBtn.clicked.connect(self.saveToCSVBtnCallback)
        self.clearPlotBtn.clicked.connect(self.clearPlotBtnCallback)
        self.exitBtn.clicked.connect(self.exitBtnCallback)
        self.setBtn.clicked.connect(self.setBtnCallback)


        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        self.resetBtn.setEnabled(False)
        self.pauseBtn.setEnabled(False)
        self.unpauseBtn.setEnabled(False)
        self.flipBtn.setEnabled(False)
        self.saveToCSVBtn.setEnabled(False)
        self.clearPlotBtn.setEnabled(False)
        self.exitBtn.setEnabled(True)
        self.setBtn.setEnabled(True)

        # ========== ENTRIES ========== # 
        self.stepEntry = QLineEdit()
        self.hRangeEntry = QLineEdit()
        self.lRangeEntry = QLineEdit()
        self.startPointEntry = QLineEdit()
        self.maxRangeEntry = QLineEdit()
        self.numOfStepsEntry = QLineEdit()

        self.stepEntry.setText(str(GEN_DEFAULT_STEP))
        self.hRangeEntry.setText(str(GEN_DEFAULT_HRANGE))
        self.lRangeEntry.setText(str(GEN_DEFAULT_LRANGE))
        self.startPointEntry.setText(str(GEN_DEFAULT_VOLTAGE))
        self.maxRangeEntry.setText(str(GEN_DEFAULT_HRANGE))
        self.numOfStepsEntry.setText(str(GEN_DEFAULT_NUM_STEPS))

        self.stepEntry.setValidator(QDoubleValidator(0.0, 1000.0, 2))
        self.hRangeEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        self.lRangeEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        self.startPointEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        self.maxRangeEntry.setValidator(QDoubleValidator(-1000.0, 1000.0, 2))
        self.numOfStepsEntry.setValidator(QIntValidator(1,20))

        # ========== COMBOBOXES ========== # 
        self.genModeCombobox = QComboBox()
        self.directionCombobox = QComboBox()
        self.gainCombobox = QComboBox()
        self.IVRatioCombobox = QComboBox()

        self.genModeCombobox.addItems(GUI_COMBOBOX_VALUES)
        self.directionCombobox.addItems(GUI_DIR_COMBOBOX_VALUES)
        self.gainCombobox.addItems(GUI_GAIN_COMBOBOX_VALUES)
        self.IVRatioCombobox.addItems(GUI_RATIO_COMBOBOX_VALUES)

        self.genModeCombobox.setCurrentIndex(0)
        self.directionCombobox.setCurrentIndex(0)
        self.gainCombobox.setCurrentIndex(0)
        self.IVRatioCombobox.setCurrentIndex(0)

        self.genModeCombobox.currentIndexChanged.connect(self.genModeCBCallback)
        self.directionCombobox.currentTextChanged.connect(self.directionCBCallback)
        self.gainCombobox.currentTextChanged.connect(self.gainCBCallback)
        self.IVRatioCombobox.currentTextChanged.connect(self.ratioCBCallback)

        # ========== PROGRESS BAR ========== # 
        self.progressBar = QProgressBar()
        self.progressBar.setRange(-1.0, 1.0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setValue(0.0) #temp

        # ========== PLOTS ========== # 
        self.acqPlotter = Plotter()
        self.genPlotter = Plotter()
        #SUBJECT TO CHANGE TODO
        self.timer = QTimer()
        self.timer.timeout.connect(self.plotterCallback)
        self.timer.start(16)

        # ========== LABELS ========== # 
        self.stepLabel = QLabel("Step value [mV]")
        self.IVRatioLabel = QLabel("I/V [A/V?]")
        self.gainLabel = QLabel("Gain mode")
        self.hRangeLabel = QLabel("High peak value [mV]")
        self.lRangeLabel = QLabel("Low peak value [mV]")
        self.startPointLabel = QLabel("Starting value [mV]") #used instead of base label and used for normal
        self.directionLabel = QLabel("Starting direction")
        self.maxRangeLabel = QLabel("Limit value [mV]")
        self.numOfStepsLabel = QLabel("No. of steps")
        self.errorLabel = QLabel("TEMP ERROR") #to be filled during program
        self.progressLabel = QLabel("TEMP 0.0") #to be filled during program

        self.errorLabel.setObjectName("red")
        self.progressLabel.setObjectName("blue")

        self.errorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        # 5 | 7 | 7 | 7 | . | . | 8 | 8 | 8 | 8 | 8 |
        # 6 | 9 | 9 | 9 | 0 | 0 | 6 | 6 | 6 | 6 | 6 |
        # 7 | 9 | 9 | 9 | 0 | 0 | 6 | 6 | 6 | 6 | 6 |
        # 8 | 9 | 9 | 9 | . | . | . | . | . | . | . |
        # 9 | 9 | 9 | 9 | . | . | . | . | . | . | . |

        
        # GRID SETTINGS --------- .addWidget(xyz, [row], [column], [rowSpan], [columnSpan])

        self.steppingSettingsLayout.addWidget(self.maxRangeLabel,     0, 0,   1, 1)
        self.steppingSettingsLayout.addWidget(self.maxRangeEntry,     0, 1,   1, 1)
        self.steppingSettingsLayout.addWidget(self.numOfStepsLabel,   1, 0,   1, 1)
        self.steppingSettingsLayout.addWidget(self.numOfStepsEntry,   1, 1,   1, 1)

        self.normalSettingsLayout.addWidget(self.hRangeLabel,         0, 0,   1, 1)
        self.normalSettingsLayout.addWidget(self.hRangeEntry,         0, 1,   1, 1)
        self.normalSettingsLayout.addWidget(self.lRangeLabel,         1, 0,   1, 1)
        self.normalSettingsLayout.addWidget(self.lRangeEntry,         1, 1,   1, 1)
        self.normalSettingsLayout.addWidget(self.directionLabel,      2, 0,   1, 1)
        self.normalSettingsLayout.addWidget(self.directionCombobox,   2, 1,   1, 1)
        
        #wrapping for stackerSettingsLayout
        self.steppingSettingsWidgetWrapper = QWidget()
        self.normalSettingsWidgetWrapper = QWidget()
        self.steppingSettingsWidgetWrapper.setLayout(self.steppingSettingsLayout)
        self.normalSettingsWidgetWrapper.setLayout(self.normalSettingsLayout)

        self.stackerSettingsLayout.addWidget(self.normalSettingsWidgetWrapper) #index 0
        self.stackerSettingsLayout.addWidget(self.steppingSettingsWidgetWrapper) #index 1

        self.commonSettingsLayout.addWidget(self.startPointLabel, 0, 0,   1, 1)
        self.commonSettingsLayout.addWidget(self.startPointEntry, 0, 1,   1, 1)
        self.commonSettingsLayout.addWidget(self.stepLabel,       1, 0,   1, 1)
        self.commonSettingsLayout.addWidget(self.stepEntry,       1, 1,   1, 1)
        self.commonSettingsLayout.addWidget(self.IVRatioLabel,    2, 0,   1, 1)
        self.commonSettingsLayout.addWidget(self.IVRatioCombobox, 2, 1,   1, 1)
        self.commonSettingsLayout.addWidget(self.gainLabel,       3, 0,   1, 1)
        self.commonSettingsLayout.addWidget(self.gainCombobox,    3, 1,   1, 1)
        
        #wrapping for settingsLayout
        self.stackerSettingsWidgetWrapper = QWidget()
        self.commonSettingsWidgetWrapper = QWidget()
        self.stackerSettingsWidgetWrapper.setLayout(self.stackerSettingsLayout)    
        self.commonSettingsWidgetWrapper.setLayout(self.commonSettingsLayout) 

        self.settingsLayout.addWidget(self.genModeCombobox,               0, 1,   1, 2)
        self.settingsLayout.addWidget(self.stackerSettingsWidgetWrapper,  1, 0,   4, 4)
        self.settingsLayout.addWidget(self.commonSettingsWidgetWrapper,   4, 0,   4, 4)
        self.settingsLayout.addWidget(self.setBtn,                        8, 1,   1, 2)

        self.buttonsLayout.addWidget(self.startBtn,       0, 0,   1, 1)
        self.buttonsLayout.addWidget(self.stopBtn,        0, 1,   1, 1)
        self.buttonsLayout.addWidget(self.resetBtn,       0, 2,   1, 1)
        self.buttonsLayout.addWidget(self.pauseBtn,       1, 0,   1, 1)
        self.buttonsLayout.addWidget(self.unpauseBtn,     1, 1,   1, 1)
        self.buttonsLayout.addWidget(self.flipBtn,        1, 2,   1, 1)
        self.buttonsLayout.addWidget(self.saveToCSVBtn,   2, 0,   1, 1)
        self.buttonsLayout.addWidget(self.clearPlotBtn,   2, 1,   1, 1)
        self.buttonsLayout.addWidget(self.exitBtn,        2, 2,   1, 1)

        self.progressLayout.addWidget(self.progressLabel)
        self.progressLayout.addWidget(self.progressBar)

        self.plotLayout.addWidget(self.acqPlotter)

        self.genPlotLayout.addWidget(self.genPlotter)

        self.errorLayout.addWidget(self.errorLabel)

        #wrapping for mainLayout
        self.settingsWidgetWrapper = QWidget()
        self.buttonsWidgetWrapper = QWidget()
        self.progressWidgetWrapper = QWidget()
        self.plotWidgetWrapper = QWidget()
        self.genPlotWidgetWrapper = QWidget()
        self.errorWidgetWrapper = QWidget()
        self.settingsWidgetWrapper.setLayout(self.settingsLayout)
        self.buttonsWidgetWrapper.setLayout(self.buttonsLayout)
        self.progressWidgetWrapper.setLayout(self.progressLayout)
        self.plotWidgetWrapper.setLayout(self.plotLayout)
        self.genPlotWidgetWrapper.setLayout(self.genPlotLayout)
        self.errorWidgetWrapper.setLayout(self.errorLayout)

        self.mainLayout.addWidget(self.settingsWidgetWrapper, 0, 0,   5, 2) #1
        self.mainLayout.addWidget(self.progressWidgetWrapper, 5, 0,   1, 3) #7
        self.mainLayout.addWidget(self.genPlotWidgetWrapper,  6, 0,   4, 3)
        self.mainLayout.addWidget(self.errorWidgetWrapper,    6, 3,   2, 2)
        self.mainLayout.addWidget(self.plotWidgetWrapper,     0, 5,   6, 5)
        self.mainLayout.addWidget(self.buttonsWidgetWrapper,  6, 5,   2, 5)

        for i in range(9):
            self.mainLayout.setRowStretch(i, 1)
            self.mainLayout.setColumnStretch(i, 1)

        self.setLayout(self.mainLayout)

class FastGUI(QWidget):
    # ========== BUTTON CALLBACKS ========== #
    startBtnCallback = Signal()
    exitBtnCallback = Signal()

    # ========== COMBOBOX CALLBACKS ========== #


    # ========== PLOTTER CALLBACKS =========== #
    

    def __init__(self):
        super().__init__()

        # ========== LAYOUTS ========== #
        self.mainLayout = QGridLayout()
        self.settingsLayout = QGridLayout()
        self.errorLayout = QHBoxLayout()
        self.buttonsLayout = QVBoxLayout()

        # ========== BUTTONS ========== #    
        self.startBtn = QPushButton("RUN")
        self.exitBtn = QPushButton("EXIT")
        
        self.startBtn.setObjectName("green")
        self.exitBtn.setObjectName("red")

        self.startBtn.clicked.connect(self.startBtnCallback)
        self.exitBtn.clicked.connect(self.exitBtnCallback)

        # ========== ENTRIES ========== # 
        self.hPointEntry = QLineEdit()
        self.lPointEntry = QLineEdit()
        self.sPointEntry = QLineEdit()
        self.freqEntry = QLineEdit()
        self.samplesEntry = QLineEdit()

        self.hPointEntry.setText(str(F_GEN_DEFAULT_HPOINT))
        self.lPointEntry.setText(str(F_GEN_DEFAULT_LPOINT))
        self.sPointEntry.setText(str(F_GEN_DEFAULT_SPOINT))
        self.freqEntry.setText(str(F_GEN_DEFAULT_FREQ))
        self.samplesEntry.setText(str(F_ACQ_DEFAULT_SAMPLES))

        self.hPointEntry.setValidator(QDoubleValidator())
        self.lPointEntry.setValidator(QDoubleValidator())
        self.sPointEntry.setValidator(QDoubleValidator())
        self.freqEntry.setValidator(QIntValidator())
        self.samplesEntry.setValidator(QIntValidator())

        # ========== COMBOBOXES ========== # 
        self.waveFormCB = QComboBox()
        self.samplesPerSecCB = QComboBox()
        self.stateCH1CB = QComboBox()
        self.stateCH2CB = QComboBox()
        self.fileTypeCB = QComboBox()

        self.waveFormCB.addItems(F_GUI_WF_COMBOBOX_VALUES)
        self.samplesPerSecCB.addItems(F_GUI_DEC_COMBOBOX_VALUES)
        self.stateCH1CB.addItems(F_GUI_STATE_COMBOBOX_VALUES)
        self.stateCH2CB.addItems(F_GUI_STATE_COMBOBOX_VALUES)
        self.fileTypeCB.addItems(F_GUI_FILETYPE_COMBOBOX_VALUES)

        self.waveFormCB.setCurrentIndex(0)
        self.samplesPerSecCB.setCurrentIndex(0)
        self.stateCH1CB.setCurrentIndex(0)
        self.stateCH2CB.setCurrentIndex(0)
        self.fileTypeCB.setCurrentIndex(0)

        # ========== PLOTS ========== # 


        # ========== LABELS ========== # 
        self.waveFormLabel = QLabel("Waveform type")
        self.hPointLabel = QLabel("High value [mV]")
        self.lPointLabel = QLabel("Low value [mV]")
        self.sPointLabel = QLabel("Starting value [mV]")
        self.freqLabel = QLabel("Frequency [Hz]")
        self.samplesPerSecLabel = QLabel("Samples per second")
        self.samplesLabel = QLabel("Number of samples to collect")
        self.stateCH1Label = QLabel("channel 1 state")
        self.stateCH2Label = QLabel("channel 2 state")
        self.fileTypeLabel = QLabel("data save file format")
        self.errorLabel = QLabel("TEMP ERROR") # to be filled

        self.errorLabel.setObjectName("red")

        # ========== LAYOUT ASSIGNMENT ========== # 
        # GRID SETTINGS --------- .addWidget(xyz, [row], [column], [rowSpan], [columnSpan])
        self.settingsLayout.addWidget(self.waveFormLabel,       0, 0, 1, 1)
        self.settingsLayout.addWidget(self.waveFormCB,          0, 1, 1, 1)
        self.settingsLayout.addWidget(self.hPointLabel,         1, 0, 1, 1)
        self.settingsLayout.addWidget(self.hPointEntry,         1, 1, 1, 1)
        self.settingsLayout.addWidget(self.lPointLabel,         2, 0, 1, 1)
        self.settingsLayout.addWidget(self.lPointEntry,         2, 1, 1, 1)
        self.settingsLayout.addWidget(self.sPointLabel,         3, 0, 1, 1)
        self.settingsLayout.addWidget(self.sPointEntry,         3, 1, 1, 1)
        self.settingsLayout.addWidget(self.freqLabel,           4, 0, 1, 1)
        self.settingsLayout.addWidget(self.freqEntry,           4, 1, 1, 1)
        self.settingsLayout.addWidget(self.samplesPerSecLabel,  5, 0, 1, 1)
        self.settingsLayout.addWidget(self.samplesPerSecCB,     5, 1, 1, 1)
        self.settingsLayout.addWidget(self.samplesLabel,        6, 0, 1, 1)
        self.settingsLayout.addWidget(self.samplesEntry,        6, 1, 1, 1)
        self.settingsLayout.addWidget(self.stateCH1Label,       7, 0, 1, 1)
        self.settingsLayout.addWidget(self.stateCH1CB,          7, 1, 1, 1)
        self.settingsLayout.addWidget(self.stateCH2Label,       8, 0, 1, 1)
        self.settingsLayout.addWidget(self.stateCH2CB,          8, 1, 1, 1)
        self.settingsLayout.addWidget(self.fileTypeLabel,       9, 0, 1, 1)
        self.settingsLayout.addWidget(self.fileTypeCB,          9, 1, 1, 1)

        self.errorLayout.addWidget(self.errorLabel)

        self.buttonsLayout.addWidget(self.startBtn)
        self.buttonsLayout.addWidget(self.exitBtn)

        #wrapping for main layout
        self.settingsWidgetWrapper = QWidget()
        self.errorWidgetWrapper = QWidget()
        self.buttonsWidgetWrapper = QWidget()
        self.settingsWidgetWrapper.setLayout(self.settingsLayout)
        self.errorWidgetWrapper.setLayout(self.errorLayout)
        self.buttonsWidgetWrapper.setLayout(self.buttonsLayout)

        self.mainLayout.addWidget(self.settingsWidgetWrapper,   0, 0, 3, 2)
        self.mainLayout.addWidget(self.errorWidgetWrapper,      0, 2, 2, 2)
        self.mainLayout.addWidget(self.buttonsWidgetWrapper,    8, 2, 1, 2)

        self.setLayout(self.mainLayout)
        
        
 

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.resize(1000,800) #TODO Fullscreen later with exit button

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


        self.fastGUI.startBtnCallback.connect(self.fast_start_BTN_CBCK)
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
    def fast_start_BTN_CBCK(self):
        self.fastGUI.startBtn.setEnabled(False)
        #logic...TODO
        self.fastGUI.startBtn.setEnabled(True)
        

    def fast_exit_BTN_CBCK(self):
        #logic...
        self.stack.setCurrentIndex(WindowType.MENU)

    # ============ SLOW GUI ============ #
    def slow_start_BTN_CBCK(self):
        self.slowGUI.startBtn.setEnabled(False)
        self.slowGUI.stopBtn.setEnabled(True)
        self.slowGUI.resetBtn.setEnabled(True)
        self.slowGUI.pauseBtn.setEnabled(True)
        self.slowGUI.flipBtn.setEnabled(True)
        self.slowGUI.saveToCSVBtn.setEnabled(True)
        self.slowGUI.clearPlotBtn.setEnabled(True)
        self.slowGUI.exitBtn.setEnabled(True)
        #logic... TODO

    def slow_stop_BTN_CBCK(self):
        self.slowGUI.stopBtn.setEnabled(False)
        self.slowGUI.startBtn.setEnabled(True)
        #logic... TODO

    def slow_reset_BTN_CBCK(self):
        #TODO
        pass

    def slow_pause_BTN_CBCK(self):
        self.slowGUI.pauseBtn.setEnabled(False)
        self.slowGUI.unpauseBtn.setEnabled(True)
        #logic... TODO
        

    def slow_unpause_BTN_CBCK(self):
        self.slowGUI.unpauseBtn.setEnabled(False)
        self.slowGUI.pauseBtn.setEnabled(True)
        #logic... TODO

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
        #logic... TODO
        self.stack.setCurrentIndex(WindowType.MENU)

    def slow_set_BTN_CBCK(self):
        # VALIDATORS WORK BAD :(
        genMode = self.slowGUI.genModeCombobox.currentIndex()
        match genMode:
            case GenModeGUI.NORMAL:
                hRange = self.slowGUI.hRangeEntry.text()
                lRange = self.slowGUI.lRangeEntry.text()
                direction = self.slowGUI.directionCombobox.currentText()
                print(hRange, lRange, direction)
            case GenModeGUI.STEP:
                maxRange = self.slowGUI.maxRangeEntry.text()
                numOfSteps = self.slowGUI.numOfStepsEntry.text()
                print(maxRange, numOfSteps)
        startPoint = self.slowGUI.startPointEntry.text()
        step = self.slowGUI.stepEntry.text()
        IVratio = self.slowGUI.IVRatioCombobox.currentText()
        gain = self.slowGUI.gainCombobox.currentText()
        print(startPoint, step, IVratio, gain)

    def slow_genMode_CB_CBCK(self):
        currentIndex = self.slowGUI.genModeCombobox.currentIndex()
        self.slowGUI.stackerSettingsLayout.setCurrentIndex(currentIndex)
        
    #probs not needed
    def slow_direction_CB_CBCK(self):
        #TODO
        pass
    #probs not needed
    def slow_gain_CB_CBCK(self):
        #TODO
        pass
    #probs not needed
    def slow_ratio_CB_CBCK(self):
        #TODO
        pass

    def slow_plotter_CBCK(self):
        self.slowGUI.acqPlotter.updatePlot()
        self.slowGUI.genPlotter.updatePlot()


    # ======================= End Callbacks ======================= #
    #IF NOT FIXED VALIDATORS
    def checkValues(uValue, uRange: tuple):
        pass

def run():
    app = QApplication(sys.argv)
    loadStyle(app)
    app.setStyle("Fusion")
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

def loadStyle(uApp):
    with open("./styles/styles.qss", "r") as file:
        uApp.setStyleSheet(file.read())