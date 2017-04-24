from dice import DiceSet

class Player:

	def __init__(self, name):
		self.name = name
		self.dice = DiceSet()

	@classmethod
	def loadFromDict(cls, data):
		player = cls(data['name'])
		player.dice = DiceSet.loadFromDict(data['dice'])
		return player

	def toDict(self):
		return {'name': self.name, 'dice': self.dice.toDict()}

	def addFromDict(self, data):
		self.dice.addFromDict(data['dice'])

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

	def testDice(self):
		print("\t\t" + self.name + ":")
		self.dice.testDice()

