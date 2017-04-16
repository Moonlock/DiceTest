from dice import DiceSet

class Player:

	def __init__(self, name):
		self.name = name
		self.dice = DiceSet()

	def addRoll(self, red, yellow):
		self.dice.addRoll(red, yellow)

	def displayCombined(self):
		print("    " + self.name + ":")
		self.dice.displayCombined()

	def displaySeparately(self):
		print("\t\t" + self.name + ":")
		self.dice.displaySeparately()

	def graphResults(self):
		self.dice.graphResults("Rolls For " + self.name)

