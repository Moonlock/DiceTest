#! /usr/bin/python

import tkMessageBox

from GUI.load import Load
from GUI.main import Main
from GUI.menu import MainMenu
from GUI.newGame import NewGame
import Tkinter as tk
from dice import DiceSet
from player import Player


class DiceTestApp(tk.Tk):
	
	class ComparisonGroup:

		def __init__(self, name):
			self.name = name
			self.dice = DiceSet()
			self.players = []
			
		def addDice(self, data):
			self.dice.addFromDict(data['dice'])
			
			for playerData in data['players']:
				groupPlayer = self.getPlayer(playerData['name'])
				if groupPlayer:
					groupPlayer.addFromDict(playerData)
				else:
					self.players.append(Player.loadFromDict(playerData))
					
		def getPlayer(self, name):
			for player in self.players:
				if player.name == name:
					return player
			return None
		
		def getRolls(self):
			return self.dice.getRolls()
		
		def getPercentages(self):
			return self.dice.getPercentages()
		
		def testDice(self):
			return self.dice.testDice()
	
	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
# 		self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
		self.attributes('-fullscreen', True)
		
		self.players = []
		self._firstPlayer = None
		self._lastplayer = None
		
		self.groups = {}
		
		self.after(100, lambda: self._setup())
		
	def addPlayer(self, name, email, colour):
		newPlayer = Player(name, email, colour)
		
		if not self.players:
			self._firstPlayer = newPlayer
		else:
			self._lastplayer.next = newPlayer
			
		newPlayer.next = self._firstPlayer
		self._lastplayer = newPlayer
		self.players.append(newPlayer)
		
	def addGroup(self, name):
		self.groups[name] = self.ComparisonGroup(name)
		
	def addToGroup(self, groupName, diceData):
		self.groups[groupName].addDice(diceData)
		

	def startNewGame(self):
		self.frames["Main"].startNewGame()
		
	def startLoadGame(self):
		self.frames["Main"].startLoadGame()
		
	def _setup(self):
		
		response = tkMessageBox.askyesno("Prevent Yakov", "Are you Yakov?")
		if response: exit()
		response = tkMessageBox.askyesno("Prevent Yakov", "Are you lying?")
		if response: exit()
		
		self.HEIGHT = self.winfo_height()
		self.WIDTH = self.winfo_width()
		
		container = tk.Frame(self);
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		frames = []
		frames.append({"class": MainMenu, "name":"MainMenu"})
		frames.append({"class": NewGame, "name":"NewGame"})
		frames.append({"class": Load, "name": "Load"})
		frames.append({"class": Main, "name":"Main"})
		
		self.frames = {}
		for f in frames:
			frame = f["class"](container, self)
			self.frames[f["name"]] = frame
			frame.grid(row=0, column=0, sticky="nesw")
		
		self.showFrame("MainMenu")
		
	def showFrame(self, name):
		frame = self.frames[name]
		frame.tkraise()
		
app = DiceTestApp()
app.mainloop()