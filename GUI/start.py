#! /usr/bin/python

import Tkinter as tk
import newGame

TITLE_FONT = ("Utopia", 60)
SUBTITLE_FONT = ("Helvetica", 30)
TEXT_FONT = ("Helvetica", 20)

class App:

	def __init__(self, master):

		self.master = master
		
		self.frame = tk.Frame(master)
		self.frame.pack()
		
		tk.Label(self.frame, text="DICE TESTER", font=TITLE_FONT, height=2
				).pack(side="top")
# 		label.bind("<Button-1>",lambda e:e.widget.quit())
			
		tk.Button(self.frame, text="New", command=self.newGame, font=TEXT_FONT, width=10
				).pack(side="top", pady=10)

		tk.Button(self.frame, text="Load", command=self.toggle, font=TEXT_FONT, width=10
				).pack(side="top", pady=10)
				
		tk.Button(self.frame, text="Quit", command=exit, font=TEXT_FONT, width=10
				).pack(side="top", pady=10)
			
	def newGame(self):
		self.frame.destroy()

		self = newGame.App(self.master)
# 		self.frame = tk.Frame(self.master)
# 		self.frame.pack()
# 		tk.Label(self.frame, text="DICE TESTER", font=TITLE_FONT, height=2
# 				).pack(side="top")
# 				
# 		tk.Button(self.frame, text="New", command=self.master.quit, font=TEXT_FONT, width=10
# 				).pack(side="top", pady=10)
				
	def toggle(self):
		print(str(root.winfo_height()) + "x" + str(root.winfo_width()))

	
root = tk.Tk()
root.geometry("%dx%d+0+0" % (root.winfo_screenwidth(), root.winfo_screenheight()))
# root.attributes('-fullscreen', True)
windowWidth = root.winfo_width()
windowHeight = root.winfo_height()

# root.attributes('-fullscreen', True)

# root.overrideredirect(1)
# root.geometry("%dx%d+0+0" % (config.WIDTH, config.HEIGHT))
# root.focus_set() # <-- move focus to this widget
# root.bind("<Escape>", root.attributes('-fullscreen', False))

app = App(root)

root.mainloop()
