#! /usr/bin/python

from PIL import Image, ImageTk

import Tkinter as tk


SUBTITLE_FONT = ("Helvetica", 30)
HEADER_FONT = ("Helvetica", 20, "bold")
TEXT_FONT = ("Helvetica", 20)
INPUT_FONT = ("Helvetica", 12)

class Main(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		self.redDie = tk.IntVar()
		self.yellowDie = tk.IntVar()
		self.graphType = tk.StringVar(value="Combined")
		self.graphDisplay = tk.StringVar(value="Number")
		self.resultsType = tk.StringVar(value="All Players")

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
		self.turnName.pack(side="top", pady=(0, self.controller.HEIGHT/16))
				
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
		tk.Button(buttonFrame, text="Skip Turn", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.skip
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
			redDie = Image.open("../images/red" + str(i) + ".png")
			redFrame.images.append(ImageTk.PhotoImage(redDie))
			
			tk.Radiobutton(redFrame, image=redFrame.images[i-1], variable=self.redDie, value=i, indicatoron=False, font=TEXT_FONT, height=44, width=44, offrelief="groove", bd=2
					).pack(side="left", padx=(20, 0))
					
			yellowDie = Image.open("../images/yellow" + str(i) + ".png")
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
		
		graphMenu = tk.OptionMenu(graphFrame, self.graphType, "Combined", "Separate", "Cycle Players", command=self.changeGraphType)
		graphMenu.grid(row=0, column=0, columnspan=2)
		graphMenu.config(font=TEXT_FONT, width=12, anchor="w")
		graphMenu['menu'].config(font=TEXT_FONT)
		
		graph = Image.open("../graph.png")
		resized = graph.resize((self.controller.WIDTH/2, self.controller.HEIGHT*2/3),Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(resized)
		canvas = tk.Canvas(graphFrame, height=self.controller.HEIGHT*2/3, width=self.controller.WIDTH/2)
		canvas.create_image(0, 0, image=photo, anchor="nw")
		canvas.image = photo
		canvas.grid(row=1, column=0, columnspan=2)
		
		tk.Radiobutton(graphFrame, text="%", variable=self.graphDisplay, value="Percent", indicatoron=False, font=TEXT_FONT, width=10, offrelief="groove", bd=2, command=self.changeGraphDisplay
				).grid(row=2, column=0)
				
		tk.Radiobutton(graphFrame, text="#", variable=self.graphDisplay, value="Number", indicatoron=False, font=TEXT_FONT, width=10, offrelief="groove", bd=2, command=self.changeGraphDisplay
				).grid(row=2, column=1)
		
		
	def submit(self):
		pass
	
	def skip(self):
		pass
	
	def end(self, oldFrame, container):
		oldFrame.destroy()
		
		resultsFrame = tk.Frame(container)
		resultsFrame.pack()
		
		resultsMenu = tk.OptionMenu(resultsFrame, self.resultsType, "All Players", "Player 1", "Player 2", command=self.changeResultsType)
		resultsMenu.grid(row=0, column=0, columnspan=3)
		resultsMenu.config(font=TEXT_FONT, width=12, anchor="w")
		resultsMenu['menu'].config(font=TEXT_FONT)
		
		results = tk.LabelFrame(resultsFrame, relief="ridge", bd=2, width=self.controller.WIDTH/3, height=self.controller.HEIGHT/2)
		results.grid(row=1, column=0, columnspan=3, pady=(0, 20))
		
		self.saveButton = tk.Button(resultsFrame, text="Save", font=TEXT_FONT, width=10, relief="groove", bd=2, command=self.save)
		self.saveButton.grid(row=2, column=0)
				
		tk.Button(resultsFrame, text="Compare", font=TEXT_FONT, width=10, relief="groove", bd=2, state="disabled"
			).grid(row=2, column=1)

		tk.Button(resultsFrame, text="Email Results", font=TEXT_FONT, width=10, relief="groove", bd=2
				).grid(row=2, column=2)
				
	def changeGraphType(self, val):
		pass
	
	def changeGraphDisplay(self):
		pass
	
	def changeResultsType(self, val):
		pass
	
	def save(self):
		self.saveButton.config(text="Saved", state="disabled")
	
	def compare(self):
		pass
	
	def email(self):
		pass
				
	def addResults(self, resultsFrame):
		tk.Label(resultsFrame, text="DIE IS RIGGED.").pack(side="top")


