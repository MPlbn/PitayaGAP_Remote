#DO NOT TOUCH
from enum import Enum, auto

class ProgramMode(Enum):    
    IDLE = auto()
    FULL_RUN = auto()
    CONT_START = auto()
    GEN_STOP = auto()
    GEN_WORK_ROUTINE = auto()
    STEPPING_START = auto()

class GeneratorMode(Enum):
    CONT = auto()
    STEPPING = auto()

FIRST_MODE: int = 1
LAST_MODE: int = 6

DEFAULT_CHANNEL = 1

ACQ_SAMPLE_SIZE: int = 50
ACQ_BUFFER_SIZE: int = 16000 #TODO CHECK REAL VALUE

PLOT_MAX_DATA_SIZE: int = 10000

GEN_DEFAULT_HRANGE: float = 1.0
GEN_DEFAULT_LRANGE: float = -1.0
GEN_DEFAULT_STEP: float = 0.1
GEN_MAX_RANGE: float = 1.0
GEN_MIN_RANGE: float = -1.0
GEN_MAX_STEP: float = 1.0
GEN_DEFAULT_STEPPING_RANGES = [0.3, 0.5, 0.7, 0.9]
GEN_DEFAULT_VOLTAGE = 0.0

GUI_DEFAULT_INTERVAL: int = 50
GUI_DEFAULT_WINDOW_SIZE = (1000,1000)
GUI_MAX_INTERVAL: int = 5000
GUI_MIN_INTERVAL: int = 5

