#! /usr/bin/python

from ecdsa.ecdsa import __main__
import os

import Tkinter as tk


TITLE_FONT = ("Helvetica", 60)
SUBTITLE_FONT = ("Helvetica", 30)
TEXT_FONT = ("Helvetica", 20)
INPUT_FONT = ("Helvetica", 12)

class App:

	def __init__(self, master):

		self.newDice = tk.BooleanVar(value=False)
# 		self.newDice.set(False)
		
		master.after(100, lambda: self.setup(master))
		
	def setup(self, master):
		self.HEIGHT = master.winfo_height()
		self.WIDTH = master.winfo_width()
		
		tk.Label(master, text="NEW GAME", font=SUBTITLE_FONT, height=2
				).pack(side="top", pady=(0, self.HEIGHT/16))
				
		outerdiceFrame = tk.Frame()
		outerdiceFrame.pack(side="left", expand=True, fill="both")
		
		diceFrame = tk.LabelFrame(outerdiceFrame, text="Select Dice", font=INPUT_FONT, relief="ridge", padx=20, pady=20)
		diceFrame.pack(side="top")
		
		outerplayerFrame = tk.Frame()
		outerplayerFrame.pack(side="left", expand=True, fill="both")

		tk.Radiobutton(diceFrame, text="Use existing dice:", variable=self.newDice, value=False, font=TEXT_FONT
				).pack(side="top", pady=(0, 20))
				
		diceList = tk.Listbox(diceFrame, height=10, width=40, font=INPUT_FONT)
		diceList.pack(side="top", pady=(0, self.HEIGHT/8))
		
		tk.Radiobutton(diceFrame, text="Create new dice:", variable=self.newDice, value=True, font=TEXT_FONT
				).pack(side="top", pady=(0, 20))
				
		diceName = tk.Text(diceFrame, height=1, width=40, font=INPUT_FONT)
		diceName.pack(side="top")

		options = os.listdir("../data")
		for option in options:
			diceList.insert(tk.END, option)
			
		#Player Frame
		
		playerFrame = tk.LabelFrame(outerplayerFrame, text="Select Players", font=INPUT_FONT, relief="ridge", padx=20, pady=20)
		playerFrame.pack(side="top")
		
		addPlayerFrame = tk.Frame(playerFrame)
		addPlayerFrame.grid(row=0, column=0, padx=(0, self.WIDTH/16))
		
		showPlayersFrame = tk.Frame(playerFrame)
		showPlayersFrame.grid(row=0, column=1)
		
		buttonFrame = tk.Frame(outerplayerFrame)
		buttonFrame.pack(side="top", anchor="e", padx=(0, self.WIDTH/32), pady=(self.HEIGHT/8, 0))
		
		tk.Label(addPlayerFrame, text="Add Player:", font=TEXT_FONT
				).grid(row=0, column=0, columnspan=2, pady=(0, 20))
				
		playerList = tk.Listbox(addPlayerFrame, height=10, width=40, font=INPUT_FONT)
		playerList.grid(row=1, column=0, columnspan=2, pady=(0,40))
		
		tk.Label(addPlayerFrame, text="Name:", font=TEXT_FONT
				).grid(row=2, column=0, pady=(0, 20))
				
		playerName = tk.Text(addPlayerFrame, height=1, width=40, font=INPUT_FONT)
		playerName.grid(row=2, column=1, pady=(0, 20))
		
		tk.Label(addPlayerFrame, text="Email:", font=TEXT_FONT
				).grid(row=3, column=0, pady=(0, 20))
		
		playerEmail = tk.Text(addPlayerFrame, height=1, width=40, font=INPUT_FONT)
		playerEmail.grid(row=3, column=1, pady=(0, 20))
		
		tk.Button(addPlayerFrame, text="Add", font=TEXT_FONT, width=10
				).grid(row=4, column=1, sticky="e")
		
		tk.Label(showPlayersFrame, text="Players (0):", font=TEXT_FONT
				).grid(row=0, column=0, columnspan=2, pady=(0, 20))
				
		chosenPlayers = tk.Listbox(showPlayersFrame, height=7, width=40, font=INPUT_FONT)
		chosenPlayers.grid(row=1, column=0, columnspan=2, pady=(0, 40))
		
		tk.Button(showPlayersFrame, text="Remove", font=TEXT_FONT, width=10
				).grid(row=2, column=0)
				
		tk.Button(showPlayersFrame, text="Clear", font=TEXT_FONT, width=10
				).grid(row=2, column=1)
				
		tk.Button(buttonFrame, text="Start", font=TEXT_FONT, width=10
				).pack(side="right")
				
		tk.Button(buttonFrame, text="Cancel", font=TEXT_FONT, width=10
				).pack(side="right")
			
	def selectNewDice(self):
		pass
				
if(__name__ == "__main__"):
	root = tk.Tk()
	root.geometry("%dx%d+0+0" % (root.winfo_screenwidth(), root.winfo_screenheight()))
	# root.attributes('-fullscreen', True)
	
	app = App(root)
	root.mainloop()


