# import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep

# define our clear function
def clear_screen():

	# for windows
	if name == 'nt':
		return system('cls')

	# for mac and linux(here, os.name is 'posix')
	else:
		return system('clear')

def bcolors():
    OK = "\u001b[32m"  # GREEN
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOR
    return (OK,WARNING,FAIL,RESET)

