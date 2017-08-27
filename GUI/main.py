from PIL import Image, ImageTk
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import smtplib
import socket

from cycler import cycler
from matplotlib import style
from matplotlib import ticker
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy

import Tkinter as tk
import config
from dice import DiceSet


style.use('seaborn-whitegrid')


matplotlib.use("TkAgg")


SUBTITLE_FONT = ("Helvetica", 30)
HEADER_FONT = ("Helvetica", 20, "bold")
TEXT_FONT = ("Helvetica", 20)
INPUT_FONT = ("Helvetica", 12)

class Main(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.filename = None
		
		self.players = self.controller.players
		self.dice = DiceSet()
		
		self.redDie = tk.IntVar()
		self.yellowDie = tk.IntVar()
		self.graphType = tk.StringVar(value="Combined")
		self.graphDisplay = tk.StringVar(value="Number")
		self.resultsType = tk.StringVar(value="All Players")
		
	def toDict(self):
		return {"dice": self.dice.toDict(), "players": [player.toDict() for player in self.controller.players]}

	def start(self):
		self.curPlayer = self.controller.players[0]
		
		self.createTitleFrame()
		
		leftFrame = tk.Frame(self)
		leftFrame.pack(side="left", expand=True, fill="both", pady=(self.controller.HEIGHT/16, 0))
		self.createInputFrame(leftFrame)
		
		rightFrame = tk.Frame(self)
		rightFrame.pack(side="left", expand=True, fill="both")
		self.createGraphFrame(rightFrame)


	def createTitleFrame(self):
		titleFrame = tk.Frame(self)
		titleFrame.pack(side="top", fill="x", anchor="n")
		
		self.rollNum = tk.Label(titleFrame, text="ROLL 0", font=SUBTITLE_FONT)
		self.rollNum.pack(side="top")
		
		self.turnName = tk.Label(titleFrame, text=self.curPlayer.name, font=SUBTITLE_FONT)
		self.turnName.pack(side="top", pady=(0, self.controller.HEIGHT/32))
				
		tk.Button(titleFrame, text="Menu", font=TEXT_FONT, width=10, relief="groove", bd=2, command=lambda: self.controller.showFrame("MainMenu")
				).place(x=20, y=20)
		
	def createInputFrame(self, leftFrame):
		inputFrame = tk.Frame(leftFrame)
		inputFrame.pack()
		
		self.createDiceFrames(inputFrame)
					
		buttonFrame = tk.Frame(inputFrame)
		buttonFrame.pack(side="top", pady=(0, self.controller.HEIGHT/8))
		
		tk.Button(buttonFrame, text="Submit", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.submit
				).grid(row=0, column=0, columnspan=2, pady=(0, 40))
		tk.Button(buttonFrame, text="Skip Turn", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.endTurn
			).grid(row=1, column=0, padx=20)
		tk.Button(buttonFrame, text="End", font=TEXT_FONT, width=10, relief="groove", bd=2, command=lambda: self.end(inputFrame, leftFrame)
				).grid(row=1, column=1, padx=20)
						
		self.createAveragesTable(inputFrame)
		
	def createDiceFrames(self, inputFrame):
		redFrame = tk.Frame(inputFrame)
		redFrame.pack(side="top", pady=(0, 20))
		redFrame.images = []
		
		yellowFrame = tk.Frame(inputFrame)
		yellowFrame.pack(side="top", pady=(0, 20))
		yellowFrame.images = []

		for i in xrange(1, 7):
			redDie = Image.open("images/red" + str(i) + ".png")
			redFrame.images.append(ImageTk.PhotoImage(redDie))
			
			tk.Radiobutton(redFrame, image=redFrame.images[i-1], variable=self.redDie, value=i, indicatoron=False, font=TEXT_FONT, height=44, width=44, offrelief="groove", bd=2
					).pack(side="left", padx=(20, 0))
					
			yellowDie = Image.open("images/yellow" + str(i) + ".png")
			yellowFrame.images.append(ImageTk.PhotoImage(yellowDie))
			
			tk.Radiobutton(yellowFrame, image=yellowFrame.images[i-1], variable=self.yellowDie, value=i, indicatoron=False, font=TEXT_FONT, height=44, width=44, offrelief="groove", bd=2
					).pack(side="left", padx=(20, 0))
					
	def createAveragesTable(self, inputFrame):
		tableFrame = tk.Frame(inputFrame, bd=2, relief="sunken")
		tableFrame.pack(side="top")
		
		titleFrame = tk.Frame(tableFrame)
		titleFrame.pack(side="top")
		tk.Label(titleFrame, text="", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=0)
		tk.Label(titleFrame, text="Red Die", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=1)
		tk.Label(titleFrame, text="Yellow Die", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=2)
		tk.Label(titleFrame, text="Combined Dice", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=3)
		
		self.allPlayersTableRow = self.createRow("All Players", tableFrame)
		for player in self.controller.players:
			player.tableRow = self.createRow(player.name, tableFrame)
			
	def createRow(self, text, tableFrame):
		row = tk.Frame(tableFrame)
		row.pack(side="top")
		
		tk.Label(row, text=text, font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=1, column=0)
		row.red = tk.Label(row, text="0", font=TEXT_FONT, bd=1, relief="ridge", width=15)
		row.yellow = tk.Label(row, text="0", font=TEXT_FONT, bd=1, relief="ridge", width=15)
		row.combined = tk.Label(row, text="0", font=TEXT_FONT, bd=1, relief="ridge", width=15)
		
		row.red.grid(row=1, column=1)
		row.yellow.grid(row=1, column=2)
		row.combined.grid(row=1, column=3)
		
		return row
					
					
	def createGraphFrame(self, rightFrame):
		graphFrame = tk.Frame(rightFrame)
		graphFrame.pack(side="top")
		
		graphOptions = ["Combined", "Separate", "Cycle Players", "----------"]
		graphOptions.extend([p.name for p in self.controller.players])

		graphMenu = tk.OptionMenu(graphFrame, self.graphType, *graphOptions, command=self.updateGraph)
		graphMenu.grid(row=0, column=0, columnspan=2)
		graphMenu.config(font=TEXT_FONT, width=12, anchor="w")
		graphMenu['menu'].config(font=TEXT_FONT)
		graphMenu['menu'].entryconfigure(3, state="disabled")
		
		self.createGraph(graphFrame)

		tk.Radiobutton(graphFrame, text="%", variable=self.graphDisplay, value="Percent", indicatoron=False, font=TEXT_FONT, width=10, offrelief="groove", bd=2, command=self.updateGraph
				).grid(row=2, column=0)
				
		tk.Radiobutton(graphFrame, text="#", variable=self.graphDisplay, value="Number", indicatoron=False, font=TEXT_FONT, width=10, offrelief="groove", bd=2, command=self.updateGraph
				).grid(row=2, column=1)
		
	def createGraph(self, frame):
		graphFrame = tk.Frame(frame, bd=3, relief="ridge")
		graphFrame.grid(row=1, column=0, columnspan=2, pady=10)
		
		colourList = [player.colour for player in self.controller.players]
		
		matplotlib.rcParams.update({'font.size': 20})
		matplotlib.rcParams.update({'axes.grid.axis': 'y'})
		matplotlib.rcParams.update({'axes.prop_cycle': cycler('color', colourList)})
		f = Figure(figsize=(9,7))
		
		self.combinedGraph = f.add_subplot(2,1,1)
		self.redGraph = f.add_subplot(2,2,3)
		self.yellowGraph = f.add_subplot(2,2,4)
		
		self.canvas = FigureCanvasTkAgg(f, graphFrame)
		self.canvas.show()
		self.canvas.get_tk_widget().pack()
		
		self.updateGraph()
		
		
	def submit(self):
		red, yellow = self.redDie.get(), self.yellowDie.get()
		if red and yellow:
			self.dice.addRoll(red, yellow)
			self.curPlayer.dice.addRoll(red, yellow)
			self.redDie.set(0)
			self.yellowDie.set(0)
			
			self.updateAverages(self.allPlayersTableRow, self.dice)
			self.updateAverages(self.curPlayer.tableRow, self.curPlayer.dice)
			self.endTurn()
			
			self.updateGraph()
			
	def updateAverages(self, row, diceSet):
		redAvg, yellowAvg, combined = diceSet.getAverages()
		row.red.config(text=str(redAvg))
		row.yellow.config(text=str(yellowAvg))
		row.combined.config(text=str(combined))
			
	def updateGraph(self, val=None):
		self.combinedGraph.clear()
		self.redGraph.clear()
		self.yellowGraph.clear()
		
		graphType = self.graphType.get()
		if graphType == "Combined":
			self.updateCombinedGraph()
		elif graphType == "Separate":
			self.updateSeparatedGraph()
		elif graphType == "Cycle Players":
			self.updateCombinedGraph(self.curPlayer)
		else:
			self.updateCombinedGraph(self.getPlayer(graphType))
			
		self.redGraph.set_xlabel("Red Die")
		self.yellowGraph.set_xlabel("Yellow Die")
		self.combinedGraph.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=5))
		self.redGraph.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=5))
		self.yellowGraph.yaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=5))
		
		if self.dice.numRolls == 0:
			self.combinedGraph.set_ylim(0, 1)
			self.redGraph.set_ylim(0, 1)
			self.yellowGraph.set_ylim(0, 1)
			self.canvas.draw()
			
		self.canvas.draw()
		
	def updateCombinedGraph(self, player=None):
		red, yellow, combined = self.getGraphData(player)
		self.combinedGraph.bar(range(2, 13), combined, color="blue", edgecolor="black", tick_label=range(2, 13))
		self.redGraph.bar(range(1, 7), red, color="red", edgecolor="black", tick_label=range(1, 7))
		self.yellowGraph.bar(range(1, 7), yellow, color="yellow", edgecolor="black", tick_label=range(1, 7))
		
	def updateSeparatedGraph(self):
		prevCombined = prevRed = prevYellow = 0
		for player in self.controller.players:
			red, yellow, combined = self.getGraphData(player, self.dice.numRolls)
			
			self.combinedGraph.bar(range(2, 13), combined, edgecolor="black", tick_label=range(2, 13), bottom=prevCombined)
			self.redGraph.bar(range(1, 7), red, edgecolor="black", tick_label=range(1, 7), bottom=prevRed)
			self.yellowGraph.bar(range(1, 7), yellow, edgecolor="black", tick_label=range(1, 7), bottom=prevYellow)
			prevCombined = numpy.add(prevCombined, combined).tolist()
			prevRed = numpy.add(prevRed, red).tolist()
			prevYellow = numpy.add(prevYellow, yellow).tolist()
			
		self.combinedGraph.legend([p.name for p in self.controller.players], ncol=min(len(self.controller.players), 4),
								loc="lower center", bbox_to_anchor=(0.5, 0.95))
		
	def getGraphData(self, player=None, numRolls=None):
		graphDisplay = self.graphDisplay.get()
		if graphDisplay == "Number":
			return player.getRolls() if player else self.dice.getRolls()
		else:
			return player.getPercentages(numRolls) if player else self.dice.getPercentages()
		
	def getPlayer(self, name):
		for player in self.controller.players:
			if player.name == name:
				return player
		return None
		
		
	def endTurn(self):
		self.curPlayer = self.curPlayer.next
		self.turnName.config(text=self.curPlayer.name)
		self.rollNum.config(text="ROLL " + str(self.dice.numRolls))
	
	def end(self, oldFrame, container):
		oldFrame.destroy()
		
		resultsFrame = tk.Frame(container)
		resultsFrame.pack()
		
		resultsOptions = ["All Players"]
		resultsOptions.extend([p.name for p in self.controller.players])
		
		resultsMenu = tk.OptionMenu(resultsFrame, self.resultsType, *resultsOptions, command=self.changeResultsType)
		resultsMenu.grid(row=0, column=0, columnspan=3)
		resultsMenu.config(font=TEXT_FONT, width=12, anchor="w")
		resultsMenu['menu'].config(font=TEXT_FONT)
		
		self.results = tk.Canvas(resultsFrame, relief="ridge", bd=2, width=self.controller.WIDTH*2/5, height=self.controller.HEIGHT/2)
		self.results.grid(row=1, column=0, columnspan=3, pady=(0, 20))
		self.results.create_text((self.controller.WIDTH/5,0), anchor="n", font=TEXT_FONT, text=self.dice.testDice())
		
		self.saveButton = tk.Button(resultsFrame, text="Save", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.save)
		self.saveButton.grid(row=2, column=0)
				
		tk.Button(resultsFrame, text="Compare", font=TEXT_FONT, width=10, relief="groove", bd=2, state="disabled", command=self.compare
			).grid(row=2, column=1)

		self.emailButton = tk.Button(resultsFrame, text="Email Results", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.tryEmailResults)
		self.emailButton.grid(row=2, column=2)
				
		self.errorMessage = tk.Label(resultsFrame, text="", font=TEXT_FONT, fg="red")
		self.errorMessage.grid(row=3, column=0, columnspan=3)
				
				
	def changeResultsType(self, val):
		self.results.delete("all")
		if val == "All Players":
			resultsText = self.dice.testDice()
		else:
			player = self.getPlayer(val)
			resultsText = player.testDice()
		
		self.results.create_text((self.controller.WIDTH/5,0), anchor="n", font=TEXT_FONT, text=resultsText)
	
	def save(self):
		f = self.getFile()
		self.filename = f.name
		
		results = self.toDict()
		json.dump(results, f)
		
		self.saveButton.config(text="Saved", state="disabled")
		
	def getFile(self):
		now = datetime.now()
		baseFilename = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
	
		i = 1
		filename = baseFilename + ".txt"
		path = "data/" + self.controller.diceName + "/"
		while os.path.exists(path + filename):
			filename = baseFilename + "_" + str(i) + ".txt"
			i += 1

		return file(path + filename, 'w')
	
	def compare(self):
		pass
	
	def tryEmailResults(self):
		try:
			self.emailResults()
		except (socket.gaierror, smtplib.SMTPServerDisconnected):
			self.displayError("No Internet connection.")
			
	def emailResults(self):
		mailserver = smtplib.SMTP(config.HOST, 587, timeout=5)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login(config.ADDRESS, config.PASSWORD)
	
		addresses = [player.email for player in self.controller.players]
		gameName = self.controller.diceName
		
		attachment = MIMEText(json.dumps(self.toDict()))
		attachment.add_header('Content-Disposition', 'attachment', filename=gameName)
	
		msg = MIMEMultipart('alternative')
		msg.attach(attachment)
		msg['Subject'] = 'Dice results - ' + gameName
		msg['From'] = config.ADDRESS
		msg['To'] = ",".join(addresses)
	
		mailserver.sendmail(config.ADDRESS, addresses, msg.as_string())
		mailserver.close()
		
		self.emailButton.config(text="Sent", state="disabled")
	
	def displayError(self, msg):
		self.errorMessage.config(text=msg)
		self.errorMessage.after(5000, self.clearError)
		
	def clearError(self):
		self.errorMessage.config(text="")
				



























