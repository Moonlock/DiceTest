import json
import os

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy

import Tkinter as tk
import matplotlib as plot


style.use('seaborn-whitegrid')


plot.use("TkAgg")


TITLE_FONT = ("Helvetica", 60)
SUBTITLE_FONT = ("Helvetica", 30)
TEXT_FONT = ("Helvetica", 20)
INPUT_FONT = ("Helvetica", 12)

class Load(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		self.gamesLoaded = {}
		
		self.createTitleFrame()
		
		leftFrame = tk.Frame(self)
		leftFrame.pack(side="left", expand=True, fill="both")
		
		topFrame = tk.Frame(leftFrame)
		topFrame.pack(side="top", expand=True, fill="both")
		self.createChooseGroupFrame(topFrame)
		
		bottomFrame = tk.Frame(leftFrame)
		bottomFrame.pack(side="top", expand=True, fill="both")
		self.createChooseGameFrame(bottomFrame)

		rightFrame = tk.Frame(self)
		rightFrame.pack(side="left", expand=True, fill="both")
		self.createPreviewFrame(rightFrame)
		
		
	def createTitleFrame(self):
		titleFrame = tk.Frame(self)
		titleFrame.pack(side="top", expand=False, fill="x", anchor="n")
		
		tk.Label(titleFrame, text="LOAD GAME", font=SUBTITLE_FONT, height=1
			).pack(side="top", pady=(20, 0))
			
		self.errorMessage = tk.Label(titleFrame, text="", font=TEXT_FONT, fg="red")
		self.errorMessage.pack(side="top")
		
		
	def createChooseGroupFrame(self, frame):
		groupFrame = tk.LabelFrame(frame, text="Select Group", font=INPUT_FONT, relief="ridge", padx=20, pady=20)
		groupFrame.pack(side="top")
		
		tk.Label(groupFrame, text="Group Name:", font=TEXT_FONT).grid(row=0, column=0)
		self.groupList = tk.Listbox(groupFrame, height=6, width=40, font=INPUT_FONT, exportselection=False)
		self.groupList.grid(row=1, column=0)
		self.groupList.bind('<<ListboxSelect>>', self.selectGroup)
		self.groupName = tk.Text(groupFrame, height=1, width=40, font=INPUT_FONT)
		self.groupName.grid(row=2, column=0, pady=(10, 0))
		tk.Button(groupFrame, text="Create Group", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.createGroup
				).grid(row=3, column=0)

		tk.Label(groupFrame, text="Games in Group:", font=TEXT_FONT).grid(row=0, column=1)
		self.gamesInGroup = tk.Listbox(groupFrame, height=10, width=40, font=INPUT_FONT, exportselection=False)
		self.gamesInGroup.grid(row=1, column=1, rowspan=3)
		
	def createChooseGameFrame(self, frame):
		gameFrame = tk.LabelFrame(frame, text="Add Game to Group", font=INPUT_FONT, relief="ridge", padx=20, pady=20)
		gameFrame.pack(side="top")
		
		tk.Label(gameFrame, text="Dice Name:", font=TEXT_FONT).grid(row=0, column=0)
		self.diceList = tk.Listbox(gameFrame, height=10, width=40, font=INPUT_FONT, exportselection=False)
		self.diceList.grid(row=1, column=0)
		self.diceList.bind('<<ListboxSelect>>', self.selectDice)
		
		options = os.listdir("data")
		for option in options:
			self.diceList.insert(tk.END, option)
		
		tk.Label(gameFrame, text="Game:", font=TEXT_FONT).grid(row=0, column=1, columnspan=2)
		self.gameList = tk.Listbox(gameFrame, height=10, width=40, font=INPUT_FONT, exportselection=False, selectmode="extended")
		self.gameList.grid(row=1, column=1, columnspan=2)
		self.gameList.bind('<<ListboxSelect>>', self.updateGraph)
		tk.Button(gameFrame, text="Add Game", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.addGame
				).grid(row=3, column=1)
		tk.Button(gameFrame, text="Add All", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.addAllGames
				).grid(row=3, column=2)
		
	def createPreviewFrame(self, frame):
		tk.Label(frame, text="Preview:", font=TEXT_FONT).pack(side='top', pady=20)
		
		graphFrame = tk.Frame(frame, bd=3, relief="ridge")
		graphFrame.pack(side="top")
		
		plot.rcParams.update({'font.size': 20})
		plot.rcParams.update({'axes.grid.axis': 'y'})
		fig = Figure(figsize=(9,7))
		
		self.combinedGraph = fig.add_subplot(2,1,1)
		self.redGraph = fig.add_subplot(2,2,3)
		self.yellowGraph = fig.add_subplot(2,2,4)
		
		self.canvas = FigureCanvasTkAgg(fig, graphFrame)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side='top')
		
		self.resetGraph(True)
		
		buttonFrame = tk.Frame(frame)
		buttonFrame.pack(side="top", anchor="e", padx=(0, self.controller.WIDTH/32), pady=(self.controller.HEIGHT/16, 0))
		self.createButtonFrame(buttonFrame)
	
	def createButtonFrame(self, buttonFrame):
		tk.Button(buttonFrame, text="Start", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.start
				).pack(side="right")
				
		tk.Button(buttonFrame, text="Cancel", font=TEXT_FONT, width=10, relief="groove", bd=2, command=lambda: self.controller.showFrame('MainMenu')
				).pack(side="right")	
	
	
	def createGroup(self):
		name = getText(self.groupName)
		if name:
			self.controller.addGroup(name)
			self.groupList.insert("end", name)
			self.controller.addGroup(name)
		else:
			self.displayError("Enter a name for the group.")
				
	def selectGroup(self, evt):
		selected = getSelected(evt.widget)
		if selected:
			self.gamesInGroup.delete(0, "end")
			
			games = self.gamesLoaded.get(selected['value'], None)
			if games:
				games.sort()
				for game in games:
					self.gamesInGroup.insert("end", game)
	
	
	def selectDice(self, evt):
		selected = getSelected(evt.widget)
		if selected:
			self.gameList.delete(0, tk.END)
			
			options = os.listdir("data/" + selected["value"])
			options.sort()
			for option in options:
				self.gameList.insert(tk.END, option)
				
	def addGame(self, gameNames=[]):
		if not gameNames:
			selected = self.gameList.curselection()
			gameNames = [self.gameList.get(i) for i in selected]
			
		if gameNames:
			groupName = getSelected(self.groupList)
			if groupName:
				groupName = groupName["value"]
				for gameName in gameNames:
					diceName = getSelected(self.diceList)["value"]
					data = json.load(file("data/" + diceName + "/" + gameName))
					self.controller.addToGroup(groupName, data)
					
					loadedGame = diceName + "/" + gameName
					if groupName in self.gamesLoaded:
						self.gamesLoaded[groupName].append(loadedGame)
					else:
						self.gamesLoaded[groupName] = [loadedGame]
					self.gamesInGroup.insert("end", loadedGame)
			else:
				self.displayError("No group selected.")
		else:
			self.displayError("No game selected.")
	
	def addAllGames(self):
		for game in self.gameList.get(0, "end"):
			self.addGame([game])


	def resetGraph(self, noData=False):
		self.combinedGraph.clear()
		self.redGraph.clear()
		self.yellowGraph.clear()
		
		self.redGraph.set_xlabel("Red Die")
		self.yellowGraph.set_xlabel("Yellow Die")
		self.combinedGraph.yaxis.set_major_locator(plot.ticker.MaxNLocator(integer=True, nbins=5))
		self.redGraph.yaxis.set_major_locator(plot.ticker.MaxNLocator(integer=True, nbins=5))
		self.yellowGraph.yaxis.set_major_locator(plot.ticker.MaxNLocator(integer=True, nbins=5))
		
		if noData:
			self.combinedGraph.set_ylim(0, 1)
			self.redGraph.set_ylim(0, 1)
			self.yellowGraph.set_ylim(0, 1)
			
			self.combinedGraph.bar(range(2, 13), numpy.zeros(11), tick_label=range(2, 13))
			self.redGraph.bar(range(1, 7), numpy.zeros(6), tick_label=range(1, 7))
			self.yellowGraph.bar(range(1, 7), numpy.zeros(6), tick_label=range(1, 7))
			
		self.canvas.draw()
			
	def updateGraph(self, evt):
		self.resetGraph()
		
		selected = getSelected(evt.widget)
		if selected:
			gameName = selected['value']
			diceName = getSelected(self.diceList)["value"]
			data = json.load(file("data/" + diceName + "/" + gameName))
			
			self.updateSeparatedGraph(data)
			
		self.canvas.draw()
		
	def updateSeparatedGraph(self, data):
		prevCombined = prevRed = prevYellow = 0
		for player in [playerData['dice'] for playerData in data['players']]:
			red = player['redDie']
			yellow = player['yellowDie']
			combined = player['rolls']
			
			self.combinedGraph.bar(range(2, 13), combined, edgecolor="black", tick_label=range(2, 13), bottom=prevCombined)
			self.redGraph.bar(range(1, 7), red, edgecolor="black", tick_label=range(1, 7), bottom=prevRed)
			self.yellowGraph.bar(range(1, 7), yellow, edgecolor="black", tick_label=range(1, 7), bottom=prevYellow)
			prevCombined = numpy.add(prevCombined, combined).tolist()
			prevRed = numpy.add(prevRed, red).tolist()
			prevYellow = numpy.add(prevYellow, yellow).tolist()
			
		self.combinedGraph.legend([playerData['name'] for playerData in data['players']], ncol=min(len(data['players']), 4),
								loc="lower center", bbox_to_anchor=(0.5, 0.95))
		
		
	def displayError(self, msg):
		self.errorMessage.config(text=msg)
		self.errorMessage.after(5000, self.clearError)
		
	def clearError(self):
		self.errorMessage.config(text="")
			
	def start(self):
		self.controller.startLoadGame()
		self.controller.showFrame('Main')
	

def getText(textWidget):
	return textWidget.get("1.0",'end-1c')

def getSelected(listbox):
	if listbox.curselection():
		index = int(listbox.curselection()[0])
		value = listbox.get(index)
		return {"index": index, "value": value}
	return None
