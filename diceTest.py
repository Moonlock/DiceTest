from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import smtplib
import socket

from blessings import Terminal
from oct2py import octave

import config
from dice import DiceSet
from player import Player


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

class ComparisonGroup:

	def __init__(self, name):
		self.name = name
		self.dice = DiceSet()
		self.players = []

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

def promptToLoad():
	response = input("Load data or start a new game? [l/n] ").lower()
	while not (response == 'n' or response == 'new'):
		if response == 'l' or response == 'load':
			loadData()
			start()
		response = input("Load data or start a new game? [l/n] ").lower()

def loadGroup():
	group = chooseGroup()

	gameName = chooseFromDir('data', "Choose a game: ")
	filename = chooseFromDir('data/' + gameName, "File to load into " + group.name + ": ")
	
	f = file('data/' + gameName + '/' + filename, 'r')
	data = json.load(f)

	group.dice.addFromDict(data['dice'])

	for dataPlayer in data['players']:
		found = False
		for groupPlayer in group.players:
			if dataPlayer['name'] == groupPlayer.name:
				groupPlayer.addFromDict(dataPlayer)
				found = True
		if not found:
			group.players.append(Player.loadFromDict(dataPlayer))

def loadData():
	gameName = chooseFromDir('data', "Choose a game: ")
	filename = chooseFromDir('data/' + gameName, "Choose a file: ")
	
	f = file('data/' + gameName + '/' + filename, 'r')
	data = json.load(f)

	env.dice = DiceSet.loadFromDict(data['dice'])

	for player in data['players']:
		env.players.append(Player.loadFromDict(player))

	end(False)

def chooseFromDir(directory, prompt):
	print("")

	options = os.listdir(directory)
	if not options:
		print("No data found.")
		exit()

	i = 0
	for option in options:
		print(str(i) + ") " + option)
		i += 1
	print("")

	while(True):
		choice = input(prompt)
		try:
			choice = int(choice)
			if choice < 0 or choice > i-1:
				raise ValueError
		except ValueError:
			print("Idiot.")
			continue
		break

	return options[choice]

def chooseGroup():
	i = 0
	for group in groups:
		print(str(i) + ") " + group.name)
		i += 1
	print(str(i) + ") [new]")
	print("")

	while(True):
		choice = input("Select a group: ")
		try:
			choice = int(choice)
			if choice < 0 or choice > i:
				raise ValueError
		except ValueError:
			print("Idiot.")
			continue
		break

	if choice == i:
		name = input("Group name: ")
		groups.append(ComparisonGroup(name))
	return groups[choice]

def getNumPlayers():
	while(True):
		numPlayers = input("How many players? ")

		try:
			numPlayers = int(numPlayers)
			return numPlayers
		except ValueError:
			print("Idiot.")

def updateGraph():
	if graphingOn:
		graphResults(currentGraphArg)


def getDieValue(dieString):
	dieVal = int(dieString)
	if dieVal < 1 or dieVal > 6:
		raise ValueError
	return dieVal

def isCommand(command):
	return command in ['help', 'combined', 'separate', 'graph', 'quit', 'load', 'test',\
					   'h', 'c', 's', 'g', 'q', 'l', 't']

def parseCommand(command, arg=""):
	if (command == 'h') or (command == 'help'): displayHelp()
	elif (command == 'c') or (command == 'combined'): displayCombined(arg)
	elif (command == 's') or (command == 'separate'): displaySeparately(arg)
	elif (command == 'g') or (command == 'graph'): graphOrChangeSettings(arg)
	elif (command == 'q') or (command == 'quit'): end(True)
	elif (command == 'l') or (command == 'load'): loadGroup()
	elif (command == 't') or (command == 'test'): testDice(arg)

def displayHelp():
	term = Terminal()

	print("")
	print("Commands:")
	print("	" + term.underline("h") + "elp				" +
		"Display this help message")
	print("")
	print("	" + term.underline("c") + "ombined [player | 'all']" +
		"	Results of both dice combined")
	print("	" + term.underline("s") + "eparate [player | 'all']" +
		"	Results of dice separately")
	print("	" + term.underline("g") + "raph [player | 'all']" +
		"	Graph results")
	print("	" + term.underline("g") + "raph	['on' | 'off']" +
		"	Update graph after every roll")
	print("")
	print("	" + term.underline("n") + "ext				" +
		"Skip current player's turn")
	print("")
	print("	" + term.underline("q") + "uit				" +
		"Proceed to statistical analysis")
	print("")

def displayCombined(playerName=""):
	if not playerName:
		env.dice.displayCombined()
		return

	if playerName == 'all':
		displayAllCombined()
		return

	if isPlayer(playerName):
		getPlayer(playerName).displayCombined()
		return

	print("Idiot.")

def displaySeparately(playerName=""):
	if not playerName:
		env.dice.displaySeparately()
		return

	if playerName == 'all':
		displayAllSeparately()
		return

	if isPlayer(playerName):
		getPlayer(playerName).displaySeparately()
		return

	print("Idiot.")

def graphOrChangeSettings(arg=""):
	global graphingOn

	if arg == 'on':
		graphingOn = True
		return
	if arg == 'off':
		graphingOn = False
		return

	graphResults(arg)

def graphResults(playerName=""):
	global currentGraphArg
	currentGraphArg = playerName

	if len(groups) > 1:
		graphGroups()
		return

	if not playerName:
		env.dice.graphResults("All Rolls")
		return

	if playerName == 'all':
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
	nameMatrix = []
	for player in env.players:
		rMatrix.append(player.dice.redDie.rolls)
		yMatrix.append(player.dice.yellowDie.rolls)
		cMatrix.append(player.dice.rolls)
		nameMatrix.append(player.name)

	octave.histogram(rMatrix, yMatrix, cMatrix, "Rolls For All Players", nameMatrix)

def graphGroups():
	rMatrix = []
	yMatrix = []
	cMatrix = []
	nameMatrix = []
	for group in groups:
		rMatrix.append(group.dice.redDie.rolls)
		yMatrix.append(group.dice.yellowDie.rolls)
		cMatrix.append(group.dice.rolls)
		nameMatrix.append(group.name)

	octave.histogram(rMatrix, yMatrix, cMatrix, "Rolls For All Groups", nameMatrix, True)

def testDice(playerName=""):
	if not playerName:
		env.dice.testDice()
		return

	if playerName == 'all':
		for player in env.players: player.testDice()
		return

	if playerName == 'groups':
		for group in groups: group.testDice()
		return

	if isPlayer(playerName):
		getPlayer(playerName).testDice()
		return

def isPlayer(playerName):
	for player in env.players:
		if player.name.lower() == playerName:
			return True
	return False

def getPlayer(playerName):
	for player in env.players:
		if player.name.lower() == playerName:
			return player

def displayAllCombined():
	for player in env.players:
		player.displayCombined()

def displayAllSeparately():
	for player in env.players:
		player.displaySeparately()

def end(promptToSave):
	global finished
	if finished: exit()
	finished = True

	env.dice.testDice()

	if promptToSave:
		response = input("Save these results? ").lower()
		while not (response == 'n' or response == 'no'):
			if response == 'y' or response == 'yes':
				saveResults()
				break
			response = input("Save these results? [y/n] ").lower()
			
		response = input("Email results? ").lower()
		while not (response == 'n' or response == 'no'):
			if response == 'y' or response == 'yes':
				emailResults()
				break
			response = input("Email results? [y/n] ").lower()

def saveResults():
	global filename
	gameName = getGameDirectory()
	f = getFile(gameName)
	filename = f.name
	
	results = {"dice": env.dice.toDict(), "players": [player.toDict() for player in env.players]}
	json.dump(results, f)
	print("Results saved.")
	
def emailResults():
	try:
		tryEmailResults()
	except (socket.gaierror, smtplib.SMTPServerDisconnected):
		print("No internets.")

		response = input("Try again? ").lower()
		while not (response == 'n' or response == 'no'):
			if response == 'y' or response == 'yes':
				emailResults()
				break
			response = input("Try again? [y/n] ").lower()

def tryEmailResults():
	mailserver = smtplib.SMTP(config.HOST, 587, timeout=5)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login(config.ADDRESS, config.PASSWORD)

	addresses = getEmailAddresses()
	gameName = filename.split("/")[-1]
	
	fp = file(filename)
	data = fp.read()
	attachment = MIMEText(data)
	attachment.add_header('Content-Disposition', 'attachment', filename=gameName)
	fp.close()

	msg = MIMEMultipart('alternative')
	msg.attach(attachment)
	msg['Subject'] = 'Dice results - ' + gameName
	msg['From'] = config.ADDRESS
	msg['To'] = ",".join(addresses)

	mailserver.sendmail(config.ADDRESS, addresses, msg.as_string())
	mailserver.close()
	print("Emails sent.")

def getEmailAddresses():
	print("Enter email addresses (blank line to end):")
	f = file('players.txt', 'r')
	emails = json.load(f)
	
	addresses = []
	
	for player in env.players:
		if player.name in emails:
			print emails[player.name]
			addresses.append(emails[player.name])
			
	addresses.extend(promptForAddresses())
	return addresses
			
	
def promptForAddresses():
	addresses = []

	response = input(" > ")
	while response:
		addresses.append(response)
		response = input(" > ")
		
	return addresses
	
def getGameDirectory():
	print("")

	games = os.listdir('data')
	if not games:
		print("No game directories found, creating a new one.")
		gameName = input("Please enter game name: ")
		os.makedirs('data/' + gameName)
		return gameName

	i = 0
	for game in games:
		print(str(i) + ") " + game)
		i += 1
	print(str(i) + ") [new]")
	print("")

	while(True):
		choice = input("Choose a game to add results to: ")
		try:
			choice = int(choice)
			if choice < 0 or choice > i:
				raise ValueError
		except ValueError:
			print("Idiot.")
			continue
		break

	if choice == i:
		gameName = input("Please enter game name: ")
		os.makedirs('data/' + gameName)
	else:
		gameName = games[choice]

	return gameName

def getFile(gameName):
	now = datetime.now()
	baseFilename = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

	i = 1
	filename = baseFilename + ".txt"
	while os.path.exists("data/" + gameName + "/" + filename):
		filename = baseFilename + "_" + str(i) + ".txt"
		i += 1

	return file("data/" + gameName + "/" + filename, 'w')

def getPrompt(player):
	if finished:
		return " > "
	else:
		return "Roll " + str(env.dice.numRolls+1) + " - " + player.name + " > "

def handleInput(inputs, player):
	if len(inputs) > 2 or len(inputs) == 0:
		print("Idiot.")
		return False

	command = inputs[0]
	arg = inputs[1] if len(inputs) == 2 else ""

	if isCommand(command):
		parseCommand(command, arg)
		return False
	elif finished:
		print("Idiot.")
		return False

	if command == 'n' or command == 'next':
		return True

	try:
		red = getDieValue(command)
		yellow = getDieValue(arg)
	except ValueError:
		print("Idiot.")
		return False
	
	player.addRoll(red, yellow)
	env.dice.addRoll(red, yellow)

	env.dice.displayCombined()
	return True

def setup():
	numPlayers = getNumPlayers()

	for player in range(numPlayers):
		name = input("Player " + str(player) + " name: ")
		env.players.append(Player(name))

	print("")
	print("(Type 'h' to list all commands)")
	print("Enter dice; red then yellow:")

def start():
	while(True):
		for player in env.players:
			global currentGraphArg

			if isPlayer(currentGraphArg):
				currentGraphArg = player.name.lower()
			updateGraph()

			successful = False
			while not successful:
				inputs = input(getPrompt(player)).lower().split(" ")
				successful = handleInput(inputs, player)



if not os.path.exists("data"):
	os.makedirs("data")

finished = False
env = ComparisonGroup("Current")
groups = [env]
currentGraphArg = ""
graphingOn = True

preventYakov()
promptToLoad()
setup()
start()



