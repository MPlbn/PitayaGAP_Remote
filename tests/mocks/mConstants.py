#DO NOT TOUCH
from enum import Enum, auto

class ProgramMode(Enum):    
    IDLE = auto()
    FULL_RUN = auto()
    CONT_START = auto()
    GEN_STOP = auto()
    GEN_WORK_ROUTINE = auto()
    STEPPING_START = auto()
    PRE_WORK_ROUTINE = auto()
    PAUSE = auto()
    UNPAUSE = auto()

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
LAST_MODE: int = 9

DEFAULT_CHANNEL = 1

ACQ_SAMPLE_SIZE: int = 50
ACQ_BUFFER_SIZE: int = 16384

PLOT_MAX_DATA_SIZE: int = 10000
PLOT_GEN_MAX_DATA_SIZE: int = 150

GEN_DEFAULT_HRANGE: float = 1.0
GEN_DEFAULT_LRANGE: float = -1.0
GEN_DEFAULT_STEP: float = 0.1
GEN_MAX_RANGE: float = 1.0
GEN_MIN_RANGE: float = -1.0
GEN_MAX_STEP: float = 1.0
GEN_DEFAULT_STEPPING_RANGES = [0.3, 0.5, 0.7, 0.9]
GEN_DEFAULT_VOLTAGE = 0.0
GEN_DEFAULT_NUM_STEPS = 4

F_GEN_DEFAULT_DEC: int = 1
F_GEN_DEFAULT_WAVEFORM: str = "SINE"
F_GEN_DEFAULT_FREQ: int = 1000
F_GEN_DEFAULT_AMPLITUDE: float = 1.0
F_GEN_DEFAULT_SAMPLES: int = 10000


GUI_DEFAULT_INTERVAL: int = 50
GUI_DEFAULT_WINDOW_SIZE = (1600,1080)
GUI_MAX_INTERVAL: int = 5000
GUI_MIN_INTERVAL: int = 5
GUI_COMBOBOX_VALUES = ("normal", "stepping")
GUI_DIR_COMBOBOX_VALUES = ("anodic", "kathodic")
GUI_RATIO_COMBOBOX_VALUES = ("1/1", "1/10", "1/100", "1/250", "1/500") #TODO To trzeba sprawdzić jakie tam są wartości
GUI_DISABLED = ["disabled"]
GUI_ENABLED = ["!disabled"]
GUI_INCREMENT_STEP = 1
GUI_DECREMENT_STEP = -1

#TODO
F_GUI_WF_COMBOBOX_VALUES = ('SINE', 'SQUARE', 'TRIANGLE', 'RAMP_UP', 'RAMP_DOWN')
F_GUI_DEC_COMBOBOX_VALUES = (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536)

F_GUI_DEFAULT_WINDOW_SIZE = (600, 400)

S_GUI_DEFAULT_WINDOW_SIZE = (400, 250)

MOCK_TIME_SLOW: float = 0.0
MOCK_TIME_SLOW_LONG: float = 0.0