import Tkinter as tk


TITLE_FONT = ("Utopia", 60)
SUBTITLE_FONT = ("Helvetica", 30)
TEXT_FONT = ("Helvetica", 20)

class MainMenu(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.frame = tk.Frame(self)
		self.frame.pack()
		
		tk.Label(self.frame, text="DICE TESTER", font=TITLE_FONT, height=2
				).pack(side="top")
			
		tk.Button(self.frame, text="New", font=TEXT_FONT, width=10, relief="groove", bd=2, command=lambda: controller.showFrame('NewGame')
				).pack(side="top", pady=10)

		tk.Button(self.frame, text="Load", font=TEXT_FONT, width=10, relief="groove", bd=2, command=lambda: controller.showFrame('Load')
				).pack(side="top", pady=10)
				
		tk.Button(self.frame, text="Quit", font=TEXT_FONT, width=10, relief="groove", bd=2, command=exit
				).pack(side="top", pady=10)

