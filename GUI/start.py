#! /usr/bin/python

import Tkinter as tk
from main import Main
from menu import MainMenu
from newGame import NewGame


class DiceTestApp(tk.Tk):
	
	class Player:
		def __init__(self, name, email):
			self.name = name
			self.email = email
			
	def __init__(self, *args, **kwargs):
		
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(), self.winfo_screenheight()))
# 		self.attributes('-fullscreen', True)
		
		self.players = []
		self._firstPlayer = None
		self._lastplayer = None
		
		self.after(100, lambda: self._setup())
		
	def addPlayer(self, name, email):
		newPlayer = self.Player(name, email)
		
		if not self.players:
			self._firstPlayer = newPlayer
		else:
			self._lastplayer.next = newPlayer
			
		newPlayer.next = self._firstPlayer
		self._lastplayer = newPlayer
		self.players.append(newPlayer)
		
	def start(self):
		self.frames["Main"].start()
		
	def _setup(self):
		self.HEIGHT = self.winfo_height()
		self.WIDTH = self.winfo_width()
		
		container = tk.Frame(self);
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		frames = []
		frames.append({"class": MainMenu, "name":"MainMenu"})
		frames.append({"class": NewGame, "name":"NewGame"})
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