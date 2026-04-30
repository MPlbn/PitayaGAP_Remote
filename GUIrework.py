import sys
import time
from PySide6.QtWidgets import ( QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, 
                               QStackedWidget, QProgressBar, QComboBox, QLabel, QLineEdit, QStackedLayout,
                                QSizePolicy )
from PySide6.QtCore import Signal, Qt, QObject, QThread, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
#Custom modules
from constants import *
import ProgramRunner
import Plotter

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
    lockBtnCallback = Signal()
    unlockBtnCallback = Signal()
    flipBtnCallback = Signal()
    saveToCSVBtnCallback = Signal()
    clearPlotBtnCallback = Signal()
    exitBtnCallback = Signal()
    setBtnCallback = Signal()

    # ========== COMBOBOX CALLBACKS ========== #
    genModeCBCallback = Signal()

    # ========== OTHER CALLBACKS ============= #
    workerUpdateProgressCallback = Signal(float)

    def __init__(self):
        super().__init__()
        # ========== PROGRAM RUNNER ========== #
        self.PRunner = ProgramRunner.ProgramRunner()

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
        self.lockBtn = QPushButton("LOCK")
        self.unlockBtn = QPushButton("UNLOCK")
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
        self.lockBtn.clicked.connect(self.lockBtnCallback)
        self.unlockBtn.clicked.connect(self.unlockBtnCallback)
        self.flipBtn.clicked.connect(self.flipBtnCallback)
        self.saveToCSVBtn.clicked.connect(self.saveToCSVBtnCallback)
        self.clearPlotBtn.clicked.connect(self.clearPlotBtnCallback)
        self.exitBtn.clicked.connect(self.exitBtnCallback)
        self.setBtn.clicked.connect(self.setBtnCallback)


        self.startBtn.setEnabled(True)
        self.stopBtn.setEnabled(False)
        self.resetBtn.setEnabled(False)
        self.lockBtn.setEnabled(False)
        self.unlockBtn.setEnabled(False)
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

        floatExp = QRegularExpression(r"^-?\d*(\.\d{0,3})?$")
        intExp = QRegularExpression(r"^-?\d*$")

        floatValidator = QRegularExpressionValidator(floatExp)
        intValidator = QRegularExpressionValidator(intExp)

        self.stepEntry.setValidator(floatValidator)
        self.hRangeEntry.setValidator(floatValidator)
        self.lRangeEntry.setValidator(floatValidator)
        self.startPointEntry.setValidator(floatValidator)
        self.maxRangeEntry.setValidator(floatValidator)
        self.numOfStepsEntry.setValidator(intValidator)

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
        self.gainCombobox.setCurrentIndex(1)
        self.IVRatioCombobox.setCurrentIndex(0)

        self.genModeCombobox.currentIndexChanged.connect(self.genModeCBCallback)

        # ========== PROGRESS BAR ========== # 
        self.progressBar = QProgressBar()
        self.progressBar.setRange(-1000, 1000)
        self.progressBar.setTextVisible(False)
        self.progressBar.setValue(0.0) #temp

        # ========== PLOTS ========== # 
        self.acqPlotter = Plotter.AcqPlotter()
        self.genPlotter = Plotter.GenPlotter()

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
        self.errorLabel = QLabel("") #to be filled during program
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
        self.buttonsLayout.addWidget(self.lockBtn,       1, 0,   1, 1)
        self.buttonsLayout.addWidget(self.unlockBtn,     1, 1,   1, 1)
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

    def start_runner(self):
        self.thread = QThread()
        self.worker = RunnerWorker(self.PRunner)
        self.worker.moveToThread(self.thread)
        self.worker.cycleDone.connect(self.workerUpdateProgressCallback)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.deleteLater)

        self.worker.start()
        self.thread.start()
    
    def stop_runner(self):
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()

class FastGUI(QWidget):
    # ========== BUTTON CALLBACKS ========== #
    startBtnCallback = Signal()
    clearPlotBtnCallback = Signal()
    exitBtnCallback = Signal()
    workerFinishedCallback = Signal()
    
    def __init__(self):
        super().__init__()
        # ========== PROGRAMRUNNER ========== #        
        self.F_PRunner = ProgramRunner.FastProgramRunner()

        # ========== LAYOUTS ========== #
        self.mainLayout = QGridLayout()
        self.settingsLayout = QGridLayout()
        self.errorLayout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()
        self.plotLayout = QVBoxLayout()

        # ========== BUTTONS ========== #    
        self.startBtn = QPushButton("RUN")
        self.clearPlotBtn = QPushButton("CLEAR PLOT")
        self.exitBtn = QPushButton("EXIT")
        
        self.startBtn.setObjectName("green")
        self.exitBtn.setObjectName("red")

        self.startBtn.clicked.connect(self.startBtnCallback)
        self.clearPlotBtn.clicked.connect(self.clearPlotBtnCallback)
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

        floatExp = QRegularExpression(r"^-?\d*(\.\d{0,3})?$")
        intExp = QRegularExpression(r"^-?\d*$")

        floatValidator = QRegularExpressionValidator(floatExp)
        intValidator = QRegularExpressionValidator(intExp)

        self.hPointEntry.setValidator(floatValidator)
        self.lPointEntry.setValidator(floatValidator)
        self.sPointEntry.setValidator(floatValidator)
        self.freqEntry.setValidator(intValidator)
        self.samplesEntry.setValidator(intValidator)

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
        self.errorLabel = QLabel("") # to be filled

        self.errorLabel.setObjectName("red")

        # ========== PLOTS ========== # 
        self.plotter = Plotter.FAcqPlotter()
        
        # ======= PROGRESS BAR ====== # 
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(True)
        self.progressBar.setValue(0.0)

        # ========== LAYOUT ASSIGNMENT ========== # 
        # GRID SETTINGS --------- .addWidget(xyz, [row], [column], [rowSpan], [columnSpan])
        self.settingsLayout.addWidget(self.waveFormLabel,       0, 0)
        self.settingsLayout.addWidget(self.waveFormCB,          0, 1)
        self.settingsLayout.addWidget(self.hPointLabel,         1, 0)
        self.settingsLayout.addWidget(self.hPointEntry,         1, 1)
        self.settingsLayout.addWidget(self.lPointLabel,         2, 0)
        self.settingsLayout.addWidget(self.lPointEntry,         2, 1)
        self.settingsLayout.addWidget(self.sPointLabel,         3, 0)
        self.settingsLayout.addWidget(self.sPointEntry,         3, 1)
        self.settingsLayout.addWidget(self.freqLabel,           4, 0)
        self.settingsLayout.addWidget(self.freqEntry,           4, 1)
        self.settingsLayout.addWidget(self.samplesPerSecLabel,  5, 0)
        self.settingsLayout.addWidget(self.samplesPerSecCB,     5, 1)
        self.settingsLayout.addWidget(self.samplesLabel,        6, 0)
        self.settingsLayout.addWidget(self.samplesEntry,        6, 1)
        self.settingsLayout.addWidget(self.stateCH1Label,       7, 0)
        self.settingsLayout.addWidget(self.stateCH1CB,          7, 1)
        self.settingsLayout.addWidget(self.stateCH2Label,       8, 0)
        self.settingsLayout.addWidget(self.stateCH2CB,          8, 1)
        self.settingsLayout.addWidget(self.fileTypeLabel,       9, 0)
        self.settingsLayout.addWidget(self.fileTypeCB,          9, 1)
        self.settingsLayout.addWidget(self.progressBar,         10,0, 1, 2)

        self.errorLayout.addWidget(self.errorLabel)

        self.buttonsLayout.addWidget(self.startBtn)
        self.buttonsLayout.addWidget(self.clearPlotBtn)
        self.buttonsLayout.addWidget(self.exitBtn)
        
        self.plotLayout.addWidget(self.plotter)

        #wrapping for main layout
        self.settingsWidgetWrapper = QWidget()
        self.errorWidgetWrapper = QWidget()
        self.buttonsWidgetWrapper = QWidget()
        self.plotWidgetWrapper = QWidget()
        self.settingsWidgetWrapper.setLayout(self.settingsLayout)
        self.errorWidgetWrapper.setLayout(self.errorLayout)
        self.buttonsWidgetWrapper.setLayout(self.buttonsLayout)
        self.plotWidgetWrapper.setLayout(self.plotLayout)

        self.settingsWidgetWrapper.setFixedWidth(350)

        self.mainLayout.addWidget(self.settingsWidgetWrapper,   0, 0, 3, 1)
        self.mainLayout.addWidget(self.errorWidgetWrapper,      0, 1, 2, 1)
        self.mainLayout.addWidget(self.buttonsWidgetWrapper,    8, 4, 1, 3)
        self.mainLayout.addWidget(self.plotWidgetWrapper,       0, 2, 8, 8)

        self.setLayout(self.mainLayout)

    def run_runner(self, uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency, uDecimation, uSamples, uCH1, uCH2, uFileType):
        self.thread = QThread()
        self.worker = FastRunnerWorker(self.F_PRunner, uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency, uDecimation, uSamples, uCH1, uCH2, uFileType)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.workerFinishedCallback)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test")
        self.resize(1000,800)

        self.stack = QStackedWidget()

        self.menuGUI = MenuGUI()
        self.slowGUI = SlowGUI()
        self.fastGUI = FastGUI()
        #self.slowGUI.PRunner.setEventFunction(self.pr_handle_event_CBCK)
    
        self.stack.addWidget(self.menuGUI)
        self.stack.addWidget(self.slowGUI)
        self.stack.addWidget(self.fastGUI)

        # ADD callbacks to the GUIS
        self.menuGUI.fastBtnCallback.connect(self.menu_F_BTN_CBCK)
        self.menuGUI.slowBtnCallback.connect(self.menu_S_BTN_CBCK)


        self.fastGUI.startBtnCallback.connect(self.fast_start_BTN_CBCK)
        self.fastGUI.clearPlotBtnCallback.connect(self.fast_clearPlot_BTN_CBCK)
        self.fastGUI.exitBtnCallback.connect(self.fast_exit_BTN_CBCK)

        self.fastGUI.workerFinishedCallback.connect(self.fast_WORKER_FINISHED_CBCK)


        self.slowGUI.startBtnCallback.connect(self.slow_start_BTN_CBCK)
        self.slowGUI.stopBtnCallback.connect(self.slow_stop_BTN_CBCK)
        self.slowGUI.resetBtnCallback.connect(self.slow_reset_BTN_CBCK)
        self.slowGUI.lockBtnCallback.connect(self.slow_lock_BTN_CBCK)
        self.slowGUI.unlockBtnCallback.connect(self.slow_unlock_BTN_CBCK)
        self.slowGUI.flipBtnCallback.connect(self.slow_flip_BTN_CBCK)
        self.slowGUI.saveToCSVBtnCallback.connect(self.slow_saveToCSV_BTN_CBCK)
        self.slowGUI.clearPlotBtnCallback.connect(self.slow_clearPlot_BTN_CBCK)
        self.slowGUI.exitBtnCallback.connect(self.slow_exit_BTN_CBCK)
        self.slowGUI.setBtnCallback.connect(self.slow_set_BTN_CBCK)
        self.slowGUI.genModeCBCallback.connect(self.slow_genMode_CB_CBCK)

        self.slowGUI.workerUpdateProgressCallback.connect(self.slow_WORKER_CYCLE_UPDATE_CBCK)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
    # ========================= Callbacks ========================= #           
    # ============ MENU ============ #
    def menu_F_BTN_CBCK(self):
        #connecting to pitaya
        self.isConnectedToPitaya = self.fastGUI.F_PRunner.startupRoutine()
        if(self.isConnectedToPitaya):
            self.fastGUI.F_PRunner.runStreamingServer()
            self.stack.setCurrentIndex(WindowType.FAST)
            #self.showFullScreen()
        else:
            print("ERROR CONNECTING TO PITAYA, TRY AGIAN...")

    def menu_S_BTN_CBCK(self):
        self.isConnectedToPitaya = self.slowGUI.PRunner.startupRoutine()
        if(self.isConnectedToPitaya):
            self.stack.setCurrentIndex(WindowType.SLOW)
            #self.showFullScreen()
            self.slowGUI.start_runner()
        else:
            print("ERROR CONNECTING TO PITAYA AND TCP SERVER, TRY AGAIN...")
            
    # ============ FAST GUI ============ #
    def fast_start_BTN_CBCK(self):
        self.fastGUI.startBtn.setEnabled(False)
        self.fastGUI.clearPlotBtn.setEnabled(False)
        self.fastGUI.progressBar.setFormat("")
        self.fastGUI.progressBar.setValue(0)
        
        errorFlag = False
        errorText = ""
        tempWaveForm = self.fastGUI.waveFormCB.currentText()
        tempDec = self.fastGUI.samplesPerSecCB.currentText()
        tempDec = F_ACQ_DEC_DICT[tempDec]
        tempStateCH1 = self.fastGUI.stateCH1CB.currentText()
        tempStateCH2 = self.fastGUI.stateCH2CB.currentText()
        tempFileType = self.fastGUI.fileTypeCB.currentText()

        tempHPoint = self.fastGUI.hPointEntry.text()
        if(tempHPoint == ""):
            tempHPoint = F_GEN_DEFAULT_HPOINT
            self.fastGUI.hPointEntry.setText(str(F_GEN_DEFAULT_HPOINT))
        else:
            tempHPoint = float(tempHPoint)
        if(tempHPoint < F_GEN_RANGE_DOWN_LIMIT or tempHPoint > F_GEN_RANGE_UP_LIMIT):
            errorFlag = True
            errorText += f'Invalid field: High Value: voltage value is out of range. The value must be between {F_GEN_RANGE_UP_LIMIT} and {F_GEN_RANGE_DOWN_LIMIT}\n'

        tempLPoint = self.fastGUI.lPointEntry.text()
        if(tempLPoint == ""):
            tempLPoint = F_GEN_DEFAULT_LPOINT
            self.fastGUI.lPointEntry.setText(str(F_GEN_DEFAULT_LPOINT))
        else:
            tempLPoint = float(tempLPoint)
        if(tempLPoint < F_GEN_RANGE_DOWN_LIMIT or tempLPoint > F_GEN_RANGE_UP_LIMIT):
            errorFlag = True
            errorText += f'Invalid field: Low Value: voltage value is out of range. The value must be between {F_GEN_RANGE_UP_LIMIT} and {F_GEN_RANGE_DOWN_LIMIT}\n'

        if(tempLPoint > tempHPoint):
            valueHolder = tempLPoint
            tempLPoint = tempHPoint
            tempHPoint = valueHolder 

        tempSPoint = self.fastGUI.sPointEntry.text()
        if(tempSPoint == ""):
            tempSPoint = F_GEN_DEFAULT_SPOINT
            self.fastGUI.sPointEntry.setText(str(F_GEN_DEFAULT_SPOINT))
        else:
            tempSPoint = float(tempSPoint)
        if(tempSPoint < tempLPoint or tempSPoint > tempHPoint):
            errorFlag = True
            errorText += f'Invalid field: Starting Value: voltage value is out of range. The value must be between set High Value and Low Value\n'

        tempFreq = self.fastGUI.freqEntry.text()
        if(tempFreq == ""):
            tempFreq = F_GEN_DEFAULT_FREQ
            self.fastGUI.freqEntry.setText(str(F_GEN_DEFAULT_FREQ))
        else:
            tempFreq = int(tempFreq)
        if(tempFreq > F_GEN_FREQ_UP_LIMIT or tempFreq < F_GEN_FREQ_DOWN_LIMIT):
            errorFlag = True
            errorText += f'Invalid field: Frequency: Frequency is out of range. The value must be between {F_GEN_FREQ_UP_LIMIT} and {F_GEN_FREQ_DOWN_LIMIT}\n'

        tempSamples = self.fastGUI.samplesEntry.text()
        if(tempSamples == ""):
            tempSamples = F_ACQ_DEFAULT_SAMPLES
            self.fastGUI.samplesEntry.setText(F_ACQ_DEFAULT_SAMPLES)
        else:
            tempSamples = int(tempSamples)
        if(tempSamples > F_ACQ_SAMPLES_UP_LIMIT or tempSamples < F_ACQ_SAMPLES_DOWN_LIMIT):
            errorFlag = True
            errorText += f'Invalid field: Samples: Number of samples is out of range. The value must be between {F_ACQ_SAMPLES_UP_LIMIT} and {F_ACQ_SAMPLES_DOWN_LIMIT}'

        if(not errorFlag):
            self.fastGUI.errorLabel.setText("")
            tempHPoint /= MV_TO_V_VALUE
            tempLPoint /= MV_TO_V_VALUE
            tempSPoint /= MV_TO_V_VALUE
            self.fastGUI.run_runner(tempWaveForm, tempHPoint, tempLPoint, tempSPoint, tempFreq, tempDec, tempSamples, tempStateCH1, tempStateCH2, tempFileType)
            self.fastGUI.progressBar.setFormat("running the streaming service...") #set value and text
            self.fastGUI.progressBar.setValue(20)
        else:
            self.fastGUI.errorLabel.setText(errorText)
        


        
    def fast_clearPlot_BTN_CBCK(self):
        self.fastGUI.plotter.clearData()

    def fast_exit_BTN_CBCK(self):
        if(not self.isConnectedToPitaya):
            self.fastGUI.F_PRunner.connect()
        self.fastGUI.F_PRunner.stopStreaming()
        self.fastGUI.F_PRunner.disconnect()
        self.isConnectedToPitaya = False
        self.stack.setCurrentIndex(WindowType.MENU)
        self.resize(1000,800) 

    def fast_WORKER_FINISHED_CBCK(self):
        data = self.fastGUI.F_PRunner.getLatestData()
        self.fastGUI.progressBar.setFormat("Gathering data...")
        self.fastGUI.progressBar.setValue(80)
        self.fastGUI.plotter.updatePlot(data[0], data[1])
        self.fastGUI.progressBar.setFormat("Done!")
        self.fastGUI.progressBar.setValue(100)
        self.fastGUI.startBtn.setEnabled(True)
        self.fastGUI.clearPlotBtn.setEnabled(True)

    # ============ SLOW GUI ============ #
    def slow_start_BTN_CBCK(self):
        self.slowGUI.startBtn.setEnabled(False)
        self.slowGUI.setBtn.setEnabled(False)
        self.slowGUI.stopBtn.setEnabled(True)
        self.slowGUI.resetBtn.setEnabled(True)
        self.slowGUI.lockBtn.setEnabled(True)
        self.slowGUI.flipBtn.setEnabled(True)
        self.slowGUI.saveToCSVBtn.setEnabled(True)
        self.slowGUI.clearPlotBtn.setEnabled(True)
        self.slowGUI.exitBtn.setEnabled(True)
        genMode = self.slowGUI.genModeCombobox.currentIndex()
        self.slow_set_BTN_CBCK() # a little jank with genmode twice, but what can You do
        self.slowGUI.PRunner.changeMode(ProgramMode.START)
        self.slowGUI.acqPlotter.start()
        self.slowGUI.genPlotter.start()
                
    def slow_stop_BTN_CBCK(self):
        self.slowGUI.stopBtn.setEnabled(False)
        self.slowGUI.lockBtn.setEnabled(False)        
        self.slowGUI.unlockBtn.setEnabled(False)
        self.slowGUI.resetBtn.setEnabled(False)
        self.slowGUI.startBtn.setEnabled(True)
        self.slowGUI.setBtn.setEnabled(True)
        self.slowGUI.PRunner.changeMode(ProgramMode.GEN_STOP)
        self.slowGUI.acqPlotter.stop()
        self.slowGUI.genPlotter.stop()

    def slow_reset_BTN_CBCK(self):
        self.slow_unlock_BTN_CBCK()
        self.slowGUI.PRunner.resetGeneratorValue()

    def slow_lock_BTN_CBCK(self):
        self.slowGUI.lockBtn.setEnabled(False)
        self.slowGUI.unlockBtn.setEnabled(True)
        self.slowGUI.PRunner.pauseContGenerator()
        
    def slow_unlock_BTN_CBCK(self):
        self.slowGUI.unlockBtn.setEnabled(False)
        self.slowGUI.lockBtn.setEnabled(True)
        self.slowGUI.PRunner.unpauseContGenerator()

    def slow_flip_BTN_CBCK(self):
        self.slowGUI.PRunner.flipGenStep()

    def slow_saveToCSV_BTN_CBCK(self):
        self.slowGUI.acqPlotter.stop()
        self.slowGUI.genPlotter.stop()
        self.slowGUI.PRunner.startSaveProcess()
        self.slowGUI.acqPlotter.start()
        self.slowGUI.genPlotter.start()

    def slow_clearPlot_BTN_CBCK(self):
        self.slowGUI.PRunner.clearPlot()

    def slow_exit_BTN_CBCK(self):
        self.slowGUI.stop_runner()
        self.slowGUI.PRunner.exit()
        self.slowGUI.PRunner.run()
        if self.isConnectedToPitaya:
            self.slowGUI.PRunner.disconnect()
        self.stack.setCurrentIndex(WindowType.MENU)
        self.resize(1000,800)         

    def slow_set_BTN_CBCK(self):
        errorFlag = False
        errorText = ""
        genMode = self.slowGUI.genModeCombobox.currentIndex()
        tempStep = self.slowGUI.stepEntry.text()
        tempStartPoint = self.slowGUI.startPointEntry.text()
        tempIVratio = self.slowGUI.IVRatioCombobox.currentText()
        tempGain = self.slowGUI.gainCombobox.currentText()

        if(tempStep == ""):
            tempStep = GEN_DEFAULT_STEP
            self.slowGUI.stepEntry.setText(str(GEN_DEFAULT_STEP))
        else:
            tempStep = float(tempStep)
        if(tempStep > GEN_MAX_STEP or tempStep < 0):
            errorFlag = True
            errorText += f'Invalid field: Step: step value is out of range. The value must be between {0} and {GEN_MAX_STEP}\n'
        #common settings
        if(tempStartPoint == ""):
            tempStartPoint = GEN_DEFAULT_VOLTAGE
            self.slowGUI.stepEntry.setText(str(GEN_DEFAULT_VOLTAGE))
        else:
            tempStartPoint = float(tempStartPoint)
        #check the start Point later depending on normal/stepping

        match genMode:
            case GenModeGUI.NORMAL:
                tempHRange = self.slowGUI.hRangeEntry.text()
                tempLRange = self.slowGUI.lRangeEntry.text()     
                tempDirection = self.slowGUI.directionCombobox.currentText()

                if(tempHRange == ""):
                    tempHRange = GEN_DEFAULT_HRANGE
                    self.slowGUI.hRangeEntry.setText(str(GEN_DEFAULT_HRANGE))
                else:
                    tempHRange = float(tempHRange)
                if(tempHRange > GEN_MAX_RANGE or tempHRange < GEN_MIN_RANGE):               
                    errorFlag = True
                    errorText += f'Invalid field: High Peak Value: value must be between {GEN_MIN_RANGE} and {GEN_MAX_RANGE}\n'    

                if(tempLRange == ""):
                    tempLRange = GEN_DEFAULT_LRANGE
                    self.slowGUI.lRangeEntry.setText(str(GEN_DEFAULT_LRANGE))
                else:
                    tempLRange = float(tempLRange)
                if(tempLRange > GEN_MAX_RANGE or tempLRange < GEN_MIN_RANGE):
                    errorFlag = True
                    errorText += f'Invalid field: Low Peak Value: value must be between {GEN_MIN_RANGE} and {GEN_MAX_RANGE}\n'

                if(tempHRange < tempLRange):
                    swapVar = tempLRange
                    tempLRange = tempHRange
                    tempHRange = swapVar   

                if(tempStartPoint > tempHRange or tempStartPoint < tempLRange):
                    errorFlag = True
                    errorText += f'Invalid field: Starting Point Value: value must be between High Peak Value and Low Peak Value'
                if(not errorFlag):
                    self.slowGUI.PRunner.setContGeneratorParameters(tempHRange/MV_TO_V_VALUE, 
                                                            tempLRange/MV_TO_V_VALUE, 
                                                            tempStep/MV_TO_V_VALUE, 
                                                            tempDirection, 
                                                            tempStartPoint/MV_TO_V_VALUE)
            
            case GenModeGUI.STEP:
                tempNumOfSteps = self.slowGUI.numOfStepsEntry.text()
                tempMaxRange = self.slowGUI.maxRangeEntry.text()

                if(tempNumOfSteps == ""):
                    tempNumOfSteps = GEN_DEFAULT_NUM_STEPS
                    self.slowGUI.numOfStepsEntry.setText(str(GEN_DEFAULT_NUM_STEPS))
                else:
                    tempNumOfSteps = int(tempNumOfSteps)
                if(tempNumOfSteps > GEN_MAX_NUM_STEPS or tempNumOfSteps <= 0):
                    errorFlag = True
                    errorText += f'Invalid field: Number of steps: value must be between {1} and {GEN_MAX_NUM_STEPS}\ns'

                if(tempMaxRange == ""):
                    tempMaxRange = GEN_DEFAULT_HRANGE
                    self.slowGUI.maxRangeEntry.setText(str(GEN_DEFAULT_HRANGE))
                else:
                    tempMaxRange = float(tempMaxRange)
                if(tempMaxRange > GEN_MAX_RANGE or tempMaxRange < GEN_MIN_RANGE):
                    errorFlag = True
                    errorText += f'Invalid field: Max range: value must be between {GEN_MIN_RANGE} and {GEN_MAX_RANGE}\n'
                
                if((tempMaxRange >= 0 and tempStartPoint > tempMaxRange)
                    or (tempMaxRange < 0 and tempStartPoint < tempMaxRange)
                    or tempStartPoint > GEN_MAX_RANGE or tempStartPoint < GEN_MIN_RANGE):
                    errorFlag = True
                    errorText += f'Invalid field: Starting Point Value: value cannot exceed bounds {GEN_MIN_RANGE} to {GEN_MAX_RANGE} and cannot go beyond Max range\n'
                if(not errorFlag):
                    self.slowGUI.PRunner.setSteppingGeneratorParameters(tempMaxRange/MV_TO_V_VALUE,
                                                                tempStartPoint/MV_TO_V_VALUE, #Maybe different base and startPoint? TODO
                                                                tempStep/MV_TO_V_VALUE,
                                                                tempNumOfSteps,
                                                                tempStartPoint/MV_TO_V_VALUE)
        if(not errorFlag):
            self.slowGUI.PRunner.setAcquisitorParameters(tempGain)
            self.slowGUI.PRunner.resetGeneratorValue()
            ratio = self.slowGUI.PRunner.processRatio(tempIVratio)
            self.slowGUI.acqPlotter.setRatio(ratio)
        self.slowGUI.errorLabel.setText(errorText)
                    
    def slow_genMode_CB_CBCK(self):
        currentIndex = self.slowGUI.genModeCombobox.currentIndex()
        self.slowGUI.stackerSettingsLayout.setCurrentIndex(currentIndex)       

    def slow_UP_KEY_CBCK(self):
        if(self.slowGUI.PRunner.getContGeneratorPauseState()):
            self.slowGUI.PRunner.manualChangeGenVoltage(GUI_INCREMENT_STEP)    

    def slow_DOWN_KEY_CBCK(self):
        if(self.slowGUI.PRunner.getContGeneratorPauseState()):
            self.slowGUI.PRunner.manualChangeGenVoltage(GUI_DECREMENT_STEP)

    def slow_WORKER_CYCLE_UPDATE_CBCK(self, uVoltage: float):
        self.slowGUI.progressBar.setValue(int(uVoltage*1000))
        self.slowGUI.progressLabel.setText(f'{uVoltage*1000:.1f} mV')
        self.slowGUI.acqPlotter.updatePlot(self.slowGUI.PRunner.AcqDataProcessor.getDataV(),
                                           self.slowGUI.PRunner.AcqDataProcessor.getDataI())
        self.slowGUI.genPlotter.updatePlot(self.slowGUI.PRunner.GenDataProcessor.getData())
        
    
    # ======================= End Callbacks ======================= #

# ============= MISC ============= # 
def loadStyle(uApp):
    with open("./styles/styles.qss", "r") as file:
        uApp.setStyleSheet(file.read())

def run():
    app = QApplication(sys.argv)
    loadStyle(app)
    app.setStyle("Fusion")
    window = App()
    window.show()
    sys.exit(app.exec())

class RunnerWorker(QObject):
    finished = Signal()
    cycleDone = Signal(float)

    def __init__(self, uProgramRuner: ProgramRunner.ProgramRunner):
        super().__init__()
        self.runner = uProgramRuner
        self.running = False

    def stop(self):
        self.running = False
    
    def start(self):
        self.running = True

    def run(self):
        while self.running:
            maxWait = 0.001 #1ms
            t0 = time.perf_counter()
            self.runner.run()
            self.cycleDone.emit(self.runner.Acquisitor.getGenVal())
            t1 = time.perf_counter()
            delta = t1 - t0
            waitVal = maxWait - delta
            if(waitVal >= 0):
                time.sleep(waitVal)
        self.finished.emit()

class FastRunnerWorker(QObject):
    finished = Signal()
    def __init__(self, uProgramRunner: ProgramRunner.FastProgramRunner, uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency, uDecimation, uSamples, uCH1, uCH2, uFileType):
        super().__init__()
        self.runner = uProgramRunner
        self.waveform = uWaveForm
        self.hPoint = uHighPoint
        self.lPoint = uLowPoint
        self.sPoint = uStartPoint
        self.freq = uFrequency
        self.dec = uDecimation
        self.samples = uSamples
        self.ch1 = uCH1
        self.ch2 = uCH2
        self.filetype = uFileType 
    
    def run(self):
        self.runner.run(self.waveform, self.hPoint, self.lPoint, self.sPoint, self.freq, self.dec, self.samples, self.ch1, self.ch2, self.filetype)
        self.finished.emit()

# =========== END MISC =========== # 