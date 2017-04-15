from player import Player
from dice import DiceSet
from oct2py import octave

# Fix input() vs raw_input() mess
try: input = raw_input
except NameError: pass

print("""DiceTest
Copyright (C) 2017 Angela Stankowski

DiceTest is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

DiceTest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
""")

def preventYakov():
	response = input("Are you Yakov? ").lower()
	while not (response == 'n' or response == 'no'):
		if response == 'y' or response == 'yes':
			exit()
		response = input("Are you Yakov? [y/n] ").lower()

	response = input("Are you lying? ").lower()
	while not (response == 'n' or response == 'no'):
		if response == 'y' or response == 'yes':
			exit()
		response = input("Are you lying? [y/n] ").lower()

def getNumPlayers():
	while(True):
		numPlayers = input("How many players? ")

		try:
			numPlayers = int(numPlayers)
			return numPlayers
		except ValueError:
			print("Idiot.")

def getDieValue(dieString):
	dieVal = int(dieString)
	if dieVal < 1 or dieVal > 6:
		raise ValueError
	return dieVal

def isCommand(command):
	return command in ['help', 'h', 'c', 's', 'g', 'cp', 'sp', \
					   'gp', 'pc', 'ps', 'pg', 'q', 'quit']

def parseCommand(command, playerName=""):
	if (command == 'h') or (command == 'help') or (command == '?'): displayHelp()
	elif command == 'c': dice.displayCombined()
	elif command == 's': dice.displaySeparately()
	elif command == 'g': graphResults()
	elif (command == 'cp') or (command == 'pc'): displayPlayerCombined(playerName)
	elif (command == 'sp') or (command == 'ps'): displayPlayerSeparately(playerName)
	elif (command == 'gp') or (command == 'pg'): graphPlayer(playerName)
	elif (command == 'q') or (command == 'quit'): end()

def displayHelp():
	print("")
	print("Commands:")
	print("	h	Display this help message")
	print("	c	Results of both dice combined")
	print("	s	Results of dice separately")
	print("	g	Graph results")
	print("			")
	print("	q	Proceed to statistical analysis")

def graphResults():
	dice.graphResults()

def displayPlayerCombined(playerName):
	if not playerName:
		displayAllCombined()
		return

	if isPlayer(playerName):
		getPlayer(playerName).displayCombined()
		return

	print("Idiot.")

def displayPlayerSeparately(playerName):
	if not playerName:
		displayAllSeparately()
		return

	if isPlayer(playerName):
		getPlayer(playerName).displaySeparately()
		return

	print("Idiot.")

def graphPlayer(playerName):
	if not playerName:
		graphAllPlayers()
		return

	if isPlayer(playerName):
		getPlayer(playerName).graphResults()
		return

	print("Idiot.")

def graphAllPlayers():
	rMatrix = []
	yMatrix = []
	cMatrix = []
	for player in players:
		rMatrix.append(player.dice.redDie.rolls)
		yMatrix.append(player.dice.yellowDie.rolls)
		cMatrix.append(player.dice.rolls)

	octave.histogram(rMatrix, yMatrix, cMatrix)

def isPlayer(playerName):
	for player in players:
		if player.name.lower() == playerName:
			return True
	return False

def getPlayer(playerName):
	for player in players:
		if player.name.lower() == playerName:
			return player

def displayAllCombined():
	for player in players:
		player.displayCombined()

def displayAllSeparately():
	for player in players:
		player.displaySeparately()

def end():
	dice.testDice()
	exit()



preventYakov()
numPlayers = getNumPlayers()

players = []
for player in range(numPlayers):
	name = input("Player " + str(player) + " name: ")
	players.append(Player(name))

dice = DiceSet()

print("")
print("(Type 'h' to list all commands)")
print("Enter dice; red then yellow:")

while(True):
	for player in players:
		successful = False
		while not successful:
			inputs = input(
				"Roll " + str(dice.numRolls+1) + " - " + 
				player.name + " > ").lower().split(" ")

			if len(inputs) > 2 or len(inputs) == 0:
				print("Idiot.")
				continue

			if len(inputs) == 1:
				if inputs[0] == 'n' or inputs[0] == 'next':
					successful = True
					continue
				if isCommand(inputs[0]):
					parseCommand(inputs[0])
				else:
					print("Idiot")
				continue

			if isCommand(inputs[0]):
				parseCommand(inputs[0], inputs[1])
				continue

			try:
				red = getDieValue(inputs[0])
				yellow = getDieValue(inputs[1])
			except ValueError:
				print("Idiot.")
				continue
			
			player.addRoll(red, yellow)
			dice.addRoll(red, yellow)

			dice.displayCombined()
			successful = True
			continue
