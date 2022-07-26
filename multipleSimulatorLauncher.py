import os
import subprocess

SIMULATOR_LIST_PATH = 'MultipleSimulatorList.txt'
CONFIGURATION_FILE_PATH = 'ProjectConfiguration.yaml'
def checkSimulatorListExist(path):
	if os.path.isfile(path):
		return True
	return false

def checkUserInputIsAcceptable(question, firstAnswer, secondAnswer):
	answer = input(question+ " " + firstAnswer +"/"+ secondAnswer + " ");
	if answer == firstAnswer:
		return True
	elif answer == secondAnswer:
		return False
	else:
		checkUserInputIsAcceptable(question,firstAnswer,secondAnswer)

def isSavedSimulatorListUsable(path):
	if checkSimulatorListExist(path):
		if checkUserInputIsAcceptable("Do you want to use existing setup?","y","n"):
			return True
		else:
			return False
	else:
		return False
class Simulator:
    def __init__(self, rawValue):
    	splitted = rawValue.split("(")
    	if len(splitted) == 3:
    		self.name = splitted[0][:-1]
    		self.version = splitted[1][:-2]
    		self.id = splitted[2][:-1]
    	else:
    		self.name = splitted[0][:-1]
    		self.version = splitted[1].split(")")
    		self.id = splitted[3][:-1]

def simulatorListGetterAndPrint():
	output = subprocess.check_output("xcrun xctrace list devices", shell=True)
	lines = output.decode("utf-8").split("\n")
	#Skip lines until Simulators
	countForSkippingUntilSimulators = 0
	for line in lines:
		countForSkippingUntilSimulators += 1
		if "== Simulators ==" in line:
			break
	lines = lines[countForSkippingUntilSimulators:]
	counterForSelectingItems = 1
	collector = []
	for line in lines:
		if line != "":
			print(str(counterForSelectingItems)+ ".) " + line)
			counterForSelectingItems += 1
			collector.append(Simulator(line))
	return collector, counterForSelectingItems