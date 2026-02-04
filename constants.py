#DO NOT TOUCH
from enum import Enum, auto

class ProgramMode(Enum):    
    IDLE = auto()
    CONT_START = auto()
    GEN_STOP = auto()
    GEN_WORK_ROUTINE = auto()
    STEPPING_START = auto()
    PRE_WORK_ROUTINE = auto()
    CSV_WORK_ROUTINE_TO_GEN = auto()
    CSV_WORK_ROUTINE_TO_IDLE = auto()

class GeneratorMode(Enum):
    CONT = auto()
    STEPPING = auto()

class PlotType(Enum):
    ACQ = auto()
    GEN = auto()

class StopType(Enum):
    STOP_RESET = auto()
    STOP_KEEP = auto()

FIRST_MODE: int = 1
LAST_MODE: int = 8

RED_PITAYA_IP = 'rp-f0ba38.local'
PROC_NAME = 'rpsa_client' #add .exe for windows
CONFIG_PATH = './streaming_app/GAPconfig.json'

CONFIG_ACQ = "adc_streaming"
CONFIG_DEC = "adc_decimation"
CONFIG_ACQ_CH1 = "channel_state_1"
CONFIG_ACQ_CH2 = "channel_state_2" 

CONFIG_GEN = "dac_streaming"
CONFIG_GEN_AMP1 = "channel_gain_1"
CONFIG_GEN_AMP2 = "channel_gain_2"
CONFIG_GEN_RATE = "dac_rate"

WF_NUM_BITS = 16
WF_SAMPLE_RATE = 44100
WF_DEFAULT_PERIODS = 1
WF_SAMPLES_IN_PERIOD = 1024

WF_SINE = "Sine"
WF_SQR = "Square"
WF_TRI = "Triangle"
WF_RMP_UP = 'Ramp up'
WF_RMP_DWN = 'Ramp down'

ACQ_SAMPLE_SIZE: int = 1 #Recommended to not go more than 100 as it starts to loose time and goes above 42ms per step; Also PLOT_MAX_DATA_SIZE would need to go up, which is taxing on PC that runs the whole program
ACQ_BUFFER_SIZE: int = 16384
ACQ_VOLTAGE_CHANNEL = 2
ACQ_CURRENT_CHANNEL = 1
ACQ_UNITS = "VOLTS"
ACQ_DATA_FORMAT = "ASCII"
ACQ_DEFAULT_GAIN = "HV" #change to ["LV"] in case of low voltage acquisition

F_ACQ_SAMPLE_SIZE: int = 16384
F_ACQ_DEFAULT_DEC: int = 1
F_ACQ_DEFAULT_SAMPLES: int = 10000

PLOT_MAX_DATA_SIZE: int = 5000
PLOT_GEN_MAX_DATA_SIZE: int = 150
PLOT_DEFAULT_RATIO: float = 1.0

GEN_DEFAULT_CHANNEL = 1
GEN_DEFAULT_HRANGE: float = 1000.0
GEN_DEFAULT_LRANGE: float = -1000.0
GEN_DEFAULT_STEP: float = 100.0
GEN_MAX_RANGE: float = 1000.0
GEN_MIN_RANGE: float = -1000.0
GEN_MAX_STEP: float = 1000.0
GEN_DEFAULT_STEPPING_RANGES = [300, 500, 700, 900]
GEN_DEFAULT_VOLTAGE = 0.0
GEN_DEFAULT_NUM_STEPS = 4

F_GEN_DEFAULT_WAVEFORM: str = WF_SINE
F_GEN_DEFAULT_FREQ: int = 1000
F_GEN_DEFAULT_AMPLITUDE: float = 1000

F_GEN_AMP_UP_LIMIT: float = 1000
F_GEN_AMP_DOWN_LIMIT: float = -1000
F_GEN_FREQ_UP_LIMIT: int = 125000000 #temp, maybe more?
F_GEN_FREQ_DOWN_LIMIT: int = 10000
F_ACQ_SAMPLES_UP_LIMIT: int = 1000000 #temp, maybe more/less?
F_ACQ_SAMPLES_DOWN_LIMIT: int = 1

GUI_DEFAULT_INTERVAL: int = 50
GUI_DEFAULT_WINDOW_SIZE = (1600,1080)
GUI_MAX_INTERVAL: int = 5000
GUI_MIN_INTERVAL: int = 5
GUI_COMBOBOX_VALUES = ("normal", "stepping")
GUI_DIR_COMBOBOX_VALUES = ("anodic", "kathodic")
GUI_RATIO_COMBOBOX_VALUES = ("1/1", "1/10", "1/100", "1/250", "1/500")
GUI_GAIN_COMBOBOX_VALUES = ("HV", "LV")
GUI_DISABLED = ["disabled"]
GUI_ENABLED = ["!disabled"]
GUI_INCREMENT_STEP = 1
GUI_DECREMENT_STEP = -1

F_GUI_WF_COMBOBOX_VALUES = (WF_SINE, WF_SQR, WF_TRI, WF_RMP_UP, WF_RMP_DWN)
F_GUI_DEC_COMBOBOX_VALUES = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536)

F_GUI_DEFAULT_WINDOW_SIZE = (1600, 1080)

S_GUI_DEFAULT_WINDOW_SIZE = (400, 250)

MV_TO_V_VALUE = 1000