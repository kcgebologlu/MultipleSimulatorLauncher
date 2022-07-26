import os

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