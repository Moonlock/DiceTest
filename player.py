from dice import DiceSet

class Player:

	def __init__(self, name, email=None, colour=None):
		self.name = name
		self.email = email
		self.colour = colour
		self.dice = DiceSet()

	@classmethod
	def loadFromDict(cls, data):
		if 'email' in data:
			player = cls(data['name'], data['email'])
		else:
			player = cls(data['name'])
		
		player.dice = DiceSet.loadFromDict(data['dice'])
		return player

	def toDict(self):
		return {'name': self.name, 'dice': self.dice.toDict()}

	def addFromDict(self, data):
		self.dice.addFromDict(data['dice'])

	def addRoll(self, red, yellow):
		self.dice.addRoll(red, yellow)
		
	def getRolls(self):
		return self.dice.getRolls()
	
	def getPercentages(self, numRolls=None):
		return self.dice.getPercentages(numRolls)

	def testDice(self):
		return self.dice.testDice()

