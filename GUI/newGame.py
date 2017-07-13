import json
import os

import Tkinter as tk


TITLE_FONT = ("Helvetica", 60)
SUBTITLE_FONT = ("Helvetica", 30)
TEXT_FONT = ("Helvetica", 20)
INPUT_FONT = ("Helvetica", 12)

class NewGame(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		self.newDice = tk.BooleanVar(value=False)
		self.playerToEmailMap = {}
		
		self.createTitleFrame()
		
		leftFrame = tk.Frame(self)
		leftFrame.pack(side="left", expand=True, fill="both")
		self.createDiceFrame(leftFrame)
		
		rightFrame = tk.Frame(self)
		rightFrame.pack(side="left", expand=True, fill="both")
		self.createPlayerFrame(rightFrame)
		
		
	def createTitleFrame(self):
		titleFrame = tk.Frame(self)
		titleFrame.pack(side="top", expand=False, fill="x", anchor="n", pady=(0, self.controller.HEIGHT/32))
		
		tk.Label(titleFrame, text="NEW GAME", font=SUBTITLE_FONT, height=2
			).pack(side="top")
			
		self.errorMessage = tk.Label(titleFrame, text="", font=TEXT_FONT, fg="red")
		self.errorMessage.pack(side="top")
		
		
	def createDiceFrame(self, frame):
		diceFrame = tk.LabelFrame(frame, text="Select Dice", font=INPUT_FONT, relief="ridge", padx=20, pady=20)
		diceFrame.pack(side="top")
		
		tk.Radiobutton(diceFrame, text="Use existing dice:", variable=self.newDice, value=False, font=TEXT_FONT
				).pack(side="top", pady=(0, 20))
		self.createDiceList(diceFrame)
		
		tk.Radiobutton(diceFrame, text="Create new dice:", variable=self.newDice, value=True, font=TEXT_FONT
				).pack(side="top", pady=(0, 20))
		self.diceName = tk.Text(diceFrame, height=1, width=40, font=INPUT_FONT)
		self.diceName.pack(side="top")
		
	def createDiceList(self, diceFrame):
		self.diceList = tk.Listbox(diceFrame, height=10, width=40, font=INPUT_FONT, exportselection=False)
		self.diceList.pack(side="top", pady=(0, self.controller.HEIGHT/8))
		
		options = os.listdir("data")
		for option in options:
			self.diceList.insert(tk.END, option)
			
			
	def createPlayerFrame(self, frame):
		playerFrame = tk.LabelFrame(frame, text="Select Players", font=INPUT_FONT, relief="ridge", padx=20, pady=20)
		playerFrame.pack(side="top")
		
		addPlayerFrame = tk.Frame(playerFrame)
		addPlayerFrame.grid(row=0, column=0, padx=(0, self.controller.WIDTH/16))
		self.createAddPlayerFrame(addPlayerFrame)
		
		showPlayersFrame = tk.Frame(playerFrame)
		showPlayersFrame.grid(row=0, column=1)
		self.createShowPlayersFrame(showPlayersFrame)
		
		buttonFrame = tk.Frame(frame)
		buttonFrame.pack(side="top", anchor="e", padx=(0, self.controller.WIDTH/32), pady=(self.controller.HEIGHT/8, 0))
		self.createButtonFrame(buttonFrame)
		
	def createAddPlayerFrame(self, addPlayerFrame):
		tk.Label(addPlayerFrame, text="Add Player:", font=TEXT_FONT
				).grid(row=0, column=0, columnspan=2, pady=(0, 20))
		self.createPlayerList(addPlayerFrame)
		
		tk.Label(addPlayerFrame, text="Name:", font=TEXT_FONT
				).grid(row=2, column=0, pady=(0, 20))
		self.playerName = tk.Text(addPlayerFrame, height=1, width=40, font=INPUT_FONT)
		self.playerName.grid(row=2, column=1, pady=(0, 20))
		
		tk.Label(addPlayerFrame, text="Email:", font=TEXT_FONT
				).grid(row=3, column=0, pady=(0, 20))
		self.playerEmail = tk.Text(addPlayerFrame, height=1, width=40, font=INPUT_FONT)
		self.playerEmail.grid(row=3, column=1, pady=(0, 20))
		
		tk.Button(addPlayerFrame, text="Add", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.addPlayer
				).grid(row=4, column=1, sticky="e")
				
	def createPlayerList(self, addPlayerFrame):
		playerList = tk.Listbox(addPlayerFrame, height=10, width=40, font=INPUT_FONT, exportselection=False)
		playerList.bind('<<ListboxSelect>>', self.selectPlayer)
		playerList.bind('<Double-Button-1>', self.addPlayer)
		playerList.grid(row=1, column=0, columnspan=2, pady=(0,40))
		
		players = json.load(file("players.txt"))
		for player in players.keys():
			playerList.insert(tk.END, player)
		
		self.playerToEmailMap = players
		
	def createShowPlayersFrame(self, showPlayersFrame):
		self.playerLabel = tk.Label(showPlayersFrame, text="Players (0):", font=TEXT_FONT)
		self.playerLabel.grid(row=0, column=0, columnspan=2, pady=(0, 20))
				
		self.chosenPlayersList = tk.Listbox(showPlayersFrame, height=7, width=40, font=INPUT_FONT)
		self.chosenPlayersList.grid(row=1, column=0, columnspan=2, pady=(0, 40))
		
		tk.Button(showPlayersFrame, text="Remove", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.removePlayer
				).grid(row=2, column=0)
				
		tk.Button(showPlayersFrame, text="Clear", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.clearPlayerList
				).grid(row=2, column=1)
				
	def createButtonFrame(self, buttonFrame):
		tk.Button(buttonFrame, text="Start", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.validateInput
				).pack(side="right")
				
		tk.Button(buttonFrame, text="Cancel", font=TEXT_FONT, width=10, relief="groove", bd=2, command=lambda: self.controller.showFrame('MainMenu')
				).pack(side="right")
		
			
	def addPlayer(self, evt=None):
		name = getText(self.playerName)
		if(name and not name in self.chosenPlayersList.get(0, tk.END)):
			self.chosenPlayersList.insert(tk.END, name)
			self.updateNumPlayers()
	
	def removePlayer(self):
		selected = getSelected(self.chosenPlayersList)
		if selected:
			self.chosenPlayersList.delete(selected["index"])
			self.updateNumPlayers()
	
	def clearPlayerList(self):
		self.chosenPlayersList.delete(0, tk.END)
		self.updateNumPlayers()
	
	def selectPlayer(self, evt):
		selected = getSelected(evt.widget)
		if selected:
			self.playerName.delete("1.0", tk.END)
			self.playerName.insert("1.0", selected["value"])
			
			self.playerEmail.delete("1.0", tk.END)
			self.playerEmail.insert("1.0", self.playerToEmailMap[selected["value"]])
	
	def updateNumPlayers(self):
		self.playerLabel.config(text="Players (" + str(self.chosenPlayersList.size()) + "):")
		
	def validateInput(self):
		diceName = self.validateDiceName()
		if not diceName:
			return
		
		if not self.chosenPlayersList.size():
			self.errorMessage.config(text="Must have at least one player.")
			return
			
		self.start(diceName)
		
	def validateDiceName(self):
		if self.newDice.get():
			diceName = getText(self.diceName)
			if not diceName:
				self.errorMessage.config(text="Please enter a dice name.")
			if os.path.exists("data/" + diceName):
				self.errorMessage.config(text="Dice name already exists.")
				return None
			os.mkdir('data/' + diceName)
		else:
			selected = getSelected(self.diceList)
			if selected:
				diceName = selected["value"]
			else:
				self.errorMessage.config(text="No dice selected.")
				return None
			
		return diceName
			
	def start(self, diceName):
		self.controller.diceName = diceName
		for i in xrange(0, self.chosenPlayersList.size()):
			name = self.chosenPlayersList.get(i)
			email = self.playerToEmailMap.get(name)
			self.controller.addPlayer(name, email)
			
		self.controller.start()
		self.controller.showFrame('Main')
	

def getText(textWidget):
	return textWidget.get("1.0",'end-1c')

def getSelected(listbox):
	if listbox.curselection():
		index = int(listbox.curselection()[0])
		value = listbox.get(index)
		return {"index": index, "value": value}
	return None

