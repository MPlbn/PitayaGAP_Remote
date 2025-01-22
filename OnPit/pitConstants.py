import rp

AGRGS_COUNT = 6 #including the name of program
GEN_WAVEFORMS = [
    rp.rp_WAVEFORM_SINE,
    rp.rp_WAVEFORM_SQUARE,
    rp.rp_WAVEFORM_TRIANGLE,
    rp.rp_WAVEFORM_RAMP_UP,
    rp.rp_WAVEFORM_RAMP_DOWN,
    rp.rp_WAVEFORM_DC,
    rp.rp_WAVEFORM_PWM,
    rp.rp_WAVEFORM_ARBITRARY,
    rp.rp_WAVEFORM_DC_NEG,
    rp.rp_WAVEFORM_SWEEP
]
BUFF_SIZE = 16384
DEFAULT_CHANNEL = rp.RP_CH_1
