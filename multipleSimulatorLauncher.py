import os
import subprocess
from joblib import Parallel, delayed
import yaml 
from yaml.loader import SafeLoader

SIMULATOR_LIST_PATH = 'MultipleSimulatorList.txt'
CONFIGURATION_FILE_PATH = 'ProjectConfiguration.yaml'
def checkSimulatorListExist(path):
	if os.path.isfile(path):
		return True
	return False

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

def checkUserWantsToAddNumber(question, finishAnswer, maxNumber):
	answer = input(str(question)+ " " +"Selected Simulator Number/ to finish add new simulator just type "+ str(finishAnswer) + " ");
	if answer == finishAnswer:
		return -2
	try:
		userSelection = int(answer)
		if userSelection > 0 and userSelection <= maxNumber:
			return userSelection
		else:
			return 0 # means that user provide a larger number then simulator list
	except:
		return -1 # false data provided by user

def selectedNumberList(maxNumber):
	userWantsToAddNewNumber = True
	selectedNumbers = set([])
	while userWantsToAddNewNumber:
		result = checkUserWantsToAddNumber("Which simulator do you want to test?","f", maxNumber)
		if result == -2:
			userWantsToAddNewNumber = False
		elif result == -1:
			print("Please provide number or type f")
		elif result == 0:
			print("Please provide a number within the simulator list number")
		else:
			selectedNumbers.add(result)
	return list(selectedNumbers)

def getTheSelectedSimulatorsInfo(items,selectedPositions):
	collector = []
	for selectedPosition in selectedPositions:
		collector.append(items[selectedPosition-1].id)
	return collector

def getSelectedSimulatorList():
	lines, maxNumber = simulatorListGetterAndPrint()
	selectedNumbers = selectedNumberList(maxNumber)
	return getTheSelectedSimulatorsInfo(lines,selectedNumbers)

def getSavedSimulatorList(path):
	return [x[:-1] for x in open(path, 'r').readlines()]

def writeNewSimulatorsIntoFile(path,simulatorList):
	file1 = open(path, 'w')
	[file1.write(x+"\n") for x in simulatorList]
	file1.close()

def getSimulatorListForLaunch(path):
	if isSavedSimulatorListUsable(path):
		return getSavedSimulatorList(path)
	else:
		print("will bring up the simulator list")
		selectedList = getSelectedSimulatorList()
		writeNewSimulatorsIntoFile(path,selectedList)
		return selectedList

#Simulator Launcher part
def createBashScriptForLaunchSimulator(simulatorId,pC):
	deneme = subprocess.check_call("sh simulatorLauncher.sh %s %s %s %s" % (simulatorId,pC.bundleIdentifier,pC.name,pC.appName), shell=True)

def runParalelSimulatorLaunchForSelectedOnes(simulatorList,projectConfiguration):
	results = Parallel(n_jobs=5)(delayed(createBashScriptForLaunchSimulator)(i,projectConfiguration) for i in simulatorList)
	print("All subprocesses is completed")

# project configuration parser
class ProjectDetails:
	def __init__(self, rawValue):
		self.name = rawValue.get("projectName")
		self.bundleIdentifier = rawValue.get("projectBundleIdentifier")
		self.appName = rawValue.get("projectAppName")
	def printDetails(self):
		print(self.name)
		print(self.bundleIdentifier)
		print(self.appName)

def getProjectConfiguration(path):
	yamlFile = open(path,'r')
	data = yaml.load(yamlFile, Loader=SafeLoader)
	return ProjectDetails(data)

# main progress 
def runner():
	selectedSimulators = getSimulatorListForLaunch(SIMULATOR_LIST_PATH)
	projectConfiguration = getProjectConfiguration(CONFIGURATION_FILE_PATH)
	runParalelSimulatorLaunchForSelectedOnes(selectedSimulators,projectConfiguration)
runner()





