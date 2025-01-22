import acq
import gen
from pitConstants import *
import rp

import sys


#ARGS PASSED:
#   GENERATOR
#       arg1 - waveform type as an int, later converted
#       arg2 - frequency as an int    
#       arg3 - amplitude as a float
#       
#   ACQUISITOR
#       arg4 - decimation as an int
#       
#   SAMPLES       
#       arg5 - number of samples as an int


if __name__ == "__main__":
    if(len(sys.argv) != AGRGS_COUNT):
        print("error: invalid number of arguments")
        sys.exit(1)


generator = gen.PitGenerator(sys.argv[1], sys.argv[2], sys.argv[3])
acquisitor = acq.PitAcquisitor(sys.argv[4])
numberOfSamples = int(sys.argv[5])    

rp.rp_Init()
generator.reset()
acquisitor.reset()

generator.setup()
acquisitor.setup()

generator.runGeneration()
#this will be in some sort of loop
acquisitor.runAcquisition()

rp.rp_Release()