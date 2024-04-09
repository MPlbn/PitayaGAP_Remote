import ProgramRunner as PR
import GUI

counter = 0

ProgramRunner = PR.ProgramRunner()
ProgramRunner.changeMode(1)

# ProgramRunner.changeMode(2)
# ProgramRunner.run()
# while(counter < 60):
#     ProgramRunner.run()
#     counter += 1
# ProgramRunner.changeMode(3)
ProgramRunner.plotFromBuffer()
ProgramRunner.exit()