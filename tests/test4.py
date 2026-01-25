import csv
import random
from datetime import datetime
#This works fine I guess, gotta test for big numbers
def generatePath():
    prefix = 'LOG'
    postfix = '.csv'
    midfix = datetime.today().strftime('%Y%m%d%H%M%S')
    return str(prefix + midfix + postfix)

def generateValues():
    valToGen = 1000
    data = []
    for i in range(0, valToGen - 1):
        data.append(random.uniform(-1, 1))
    return data

dataOne = generateValues()
dataTwo = generateValues()

NdataOne = []
NdataTwo = []

generatedPath = generatePath()

print(generatedPath)

with open(generatedPath, 'w', newline='') as testFile:
    writer = csv.writer(testFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
    for i in range(0, len(dataOne) - 1):
        writer.writerow([dataOne[i], dataTwo[i]])

# with open(generatedPath, 'r', newline='') as testFileTwo:
#     reader = csv.reader(testFileTwo, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
#     NdataOne = next(reader)
#     NdataTwo = next(reader)

# for i in range(0, 100):
#     print(NdataOne[i])