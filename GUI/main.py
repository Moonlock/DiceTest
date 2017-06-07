#! /usr/bin/python

from PIL import Image, ImageTk
import os

import Tkinter as tk


SUBTITLE_FONT = ("Helvetica", 30)
HEADER_FONT = ("Helvetica", 20, "bold")
TEXT_FONT = ("Helvetica", 20)
INPUT_FONT = ("Helvetica", 12)

class App:

	def __init__(self, master):
		
		self.redDie = tk.IntVar()
		self.yellowDie = tk.IntVar()
		self.graphType = tk.StringVar(value="Combined")
		self.graphDisplay = tk.StringVar(value="Number")
		self.resultsType = tk.StringVar(value="All Players")

		master.after(100, lambda: self.setup(master))
		
	def setup(self, master):
		self.HEIGHT = master.winfo_height()
		self.WIDTH = master.winfo_width()
		
		tk.Label(master, text="ROLL 0", font=SUBTITLE_FONT, height=1
				).pack(side="top")
		tk.Label(master, text="[Player Name]", font=SUBTITLE_FONT, height=1
				).pack(side="top", pady=(0, self.HEIGHT/16))
				
		self.leftFrame = tk.Frame()
		self.leftFrame.pack(side="left", expand=True, fill="both", pady=(self.HEIGHT/16, 0))
				
		self.inputFrame = tk.Frame(self.leftFrame)
		self.inputFrame.pack()
		
		graphFrame = tk.Frame()
		graphFrame.pack(side="left", expand=True, fill="both")
		
		redFrame = tk.Frame(self.inputFrame)
		redFrame.pack(side="top", pady=(0, 20))
		
		yellowFrame = tk.Frame(self.inputFrame)
		yellowFrame.pack(side="top", pady=(0, 20))
		
		dieImage = tk.Frame(redFrame, height=25, width=25, bg="red")
		dieImage.pack(side="left")
		
		for i in xrange(1, 7):
			tk.Radiobutton(redFrame, text=str(i), variable=self.redDie, value=i, indicatoron=False, width=3, font=TEXT_FONT
					).pack(side="left", padx=(20, 0))
					
		dieImage = tk.Frame(yellowFrame, width=25, height=25, bg="yellow")
		dieImage.pack(side="left")
		
		for i in xrange(1, 7):
			tk.Radiobutton(yellowFrame, text=str(i), variable=self.yellowDie, value=i, indicatoron=False, width=3, font=TEXT_FONT
					).pack(side="left", padx=(20, 0))
					
		buttonFrame = tk.Frame(self.inputFrame)
		buttonFrame.pack(side="top", pady=(0, self.HEIGHT/8))
		
		tk.Button(buttonFrame, text="Submit", font=TEXT_FONT, width=10
				).grid(row=0, column=0, columnspan=2, pady=(0, 40))
				
		tk.Button(buttonFrame, text="Skip Turn", font=TEXT_FONT, width=10
			).grid(row=1, column=0, padx=20)

		tk.Button(buttonFrame, text="End", font=TEXT_FONT, width=10, command=self.end
				).grid(row=1, column=1, padx=20)
						
		tableFrame = tk.Frame(self.inputFrame, bd=2, relief="sunken")
		tableFrame.pack(side="top")
		
		tk.Label(tableFrame, text="", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=0)
		tk.Label(tableFrame, text="Red Die", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=1)
		tk.Label(tableFrame, text="Yellow Die", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=2)
		tk.Label(tableFrame, text="Combined Dice", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=0, column=3)
		
		tk.Label(tableFrame, text="Average", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=1, column=0)
		tk.Label(tableFrame, text="3.8", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=1, column=1)
		tk.Label(tableFrame, text="2.7", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=1, column=2)
		tk.Label(tableFrame, text="7.1", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=1, column=3)
		
		tk.Label(tableFrame, text="Player 1", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=2, column=0)
		tk.Label(tableFrame, text="3", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=2, column=1)
		tk.Label(tableFrame, text="3", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=2, column=2)
		tk.Label(tableFrame, text="7", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=2, column=3)
		
		tk.Label(tableFrame, text="Player 2", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=3, column=0)
		tk.Label(tableFrame, text="4.2", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=3, column=1)
		tk.Label(tableFrame, text="4.9", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=3, column=2)
		tk.Label(tableFrame, text="9.3", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=3, column=3)
		
		tk.Label(tableFrame, text="Player 2", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=4, column=0)
		tk.Label(tableFrame, text="4.2", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=4, column=1)
		tk.Label(tableFrame, text="4.9", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=4, column=2)
		tk.Label(tableFrame, text="9.3", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=4, column=3)
		
		tk.Label(tableFrame, text="Player 2", font=HEADER_FONT, bd=1, relief="ridge", width=15).grid(row=5, column=0)
		tk.Label(tableFrame, text="4.2", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=5, column=1)
		tk.Label(tableFrame, text="4.9", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=5, column=2)
		tk.Label(tableFrame, text="9.3", font=TEXT_FONT, bd=1, relief="ridge", width=15).grid(row=5, column=3)
		
		innerGraphFrame = tk.Frame(graphFrame)
		innerGraphFrame.pack(side="top")
		
		graphMenu = tk.OptionMenu(innerGraphFrame, self.graphType, "Combined", "Separate", "Cycle Players", command=self.test)
		graphMenu.grid(row=0, column=0, columnspan=2)
		graphMenu.config(font=TEXT_FONT, width=12, anchor="w")
		graphMenu['menu'].config(font=TEXT_FONT)
		
		graph = Image.open("../graph.png")
		resized = graph.resize((self.WIDTH/2, self.HEIGHT*2/3),Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(resized)
		canvas = tk.Canvas(innerGraphFrame, height=self.HEIGHT*2/3, width=self.WIDTH/2)
		canvas.create_image(0, 0, image=photo, anchor="nw")
		canvas.image = photo
		canvas.grid(row=1, column=0, columnspan=2)
		
		tk.Radiobutton(innerGraphFrame, text="%", variable=self.graphDisplay, value="Percent", indicatoron=False, font=TEXT_FONT, width=10, offrelief="groove", bd=2
				).grid(row=2, column=0)
				
		tk.Radiobutton(innerGraphFrame, text="#", variable=self.graphDisplay, value="Number", indicatoron=False, font=TEXT_FONT, width=10, offrelief="groove", bd=2
				).grid(row=2, column=1)
		
	def test(self, val):
		print val
		
	def end(self):
		self.inputFrame.destroy()
		
		resultsFrame = tk.Frame(self.leftFrame)
		resultsFrame.pack()
		
		resultsMenu = tk.OptionMenu(resultsFrame, self.resultsType, "All Players", "Player 1", "Player 2", command=self.test)
		resultsMenu.grid(row=0, column=0, columnspan=3)
		resultsMenu.config(font=TEXT_FONT, width=12, anchor="w")
		resultsMenu['menu'].config(font=TEXT_FONT)
		
		self.results = tk.LabelFrame(resultsFrame, relief="ridge", bd=2, width=self.WIDTH/3, height=self.HEIGHT/2)
		self.results.grid(row=1, column=0, columnspan=3, pady=(0, 20))
		
		tk.Button(resultsFrame, text="Save", font=TEXT_FONT, width=10, command=self._addResults
				).grid(row=2, column=0)
				
		tk.Button(resultsFrame, text="Compare", font=TEXT_FONT, width=10
			).grid(row=2, column=1)

		tk.Button(resultsFrame, text="Email Results", font=TEXT_FONT, width=10
				).grid(row=2, column=2)
				
	def _addResults(self):
		tk.Label(self.results, text="DIE IS RIGGED.").pack(side="top")
		
				
root = tk.Tk()
root.geometry("%dx%d+0+0" % (root.winfo_screenwidth(), root.winfo_screenheight()))
# root.attributes('-fullscreen', True)

# im = Image.open("../pictures/Table2.png")
# tkimage = ImageTk.PhotoImage(im)
# background_label = tk.Label(root, image=tkimage)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

app = App(root)
root.mainloop()


