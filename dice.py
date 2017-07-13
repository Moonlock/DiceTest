import numpy
from oct2py import octave


def getPValue(chiSquare):
	if chiSquare <= 1.61:
		return [0.9, 1]
	if chiSquare <= 2.675:
		return [0.75, 0.9]
	if chiSquare <= 4.351:
		return [0.50, 0.75]
	if chiSquare <= 6.626:
		return [0.25, 0.5]
	if chiSquare <= 9.236:
		return [0.1, 0.25]
	if chiSquare <= 11.07:
		return [0.05, 0.1]
	if chiSquare <= 12.83:
		return [0.025, 0.05]
	if chiSquare <= 15.086:
		return [0.01, 0.025]

	return [0, 0.01]

class Die:

	def __init__(self, rolls=None):
		self.rolls = rolls if rolls else numpy.zeros(6).tolist()
		self.numRolls = sum(self.rolls)

	def addRolls(self, rolls):
		self.rolls = numpy.add(self.rolls, rolls).tolist()
		self.numRolls = sum(self.rolls)
		
	def addRoll(self, roll):
		self.rolls[roll-1] += 1
		self.numRolls += 1
		
	def getAverage(self):
		total = 0
		for i in xrange(0, 6):
			total += self.rolls[i] * (i+1)
			
		return round(float(total) / float(self.numRolls), 2)

	def getChiSquare(self):
		expected = float(self.numRolls) / 6.0

		chiSquare = 0.0
		for i in range(6):
			chiSquare += pow(self.rolls[i] - expected, 2) / expected

		return chiSquare

	def testDie(self, colour):
# 		return 
		pValue = getPValue(self.getChiSquare())
		if pValue[1] <= 0.05:
			return (colour + " die seems to be rigged.\t" +
				"( " + str(pValue[0]) + " > p > " + str(pValue[1]) + " )\n")
		else:
			return (colour + " die does not seem to be rigged.\t" +
				"( " + str(pValue[0]) + " > p > " + str(pValue[1]) + " )\n")


class DiceSet:

	def __init__(self):
		self.redDie = Die()
		self.yellowDie = Die()
		self.rolls = numpy.zeros(11).tolist()
		self.numRolls = 0

	@classmethod
	def loadFromDict(cls, data):
		dice = DiceSet()
		dice.redDie = Die(data['redDie'])
		dice.yellowDie = Die(data['yellowDie'])
		dice.rolls = data['rolls']
		dice.numRolls = sum(dice.rolls)
		return dice

	def toDict(self):
		return {'rolls': self.rolls, 'redDie': self.redDie.rolls, 'yellowDie': self.yellowDie.rolls}

	def addFromDict(self, data):
		self.redDie.addRolls(data['redDie'])
		self.yellowDie.addRolls(data['yellowDie'])
		self.rolls = numpy.add(self.rolls, data['rolls']).tolist()
		self.numRolls = sum(self.rolls)

	def addRoll(self, red, yellow):
		self.redDie.addRoll(red)
		self.yellowDie.addRoll(yellow)

		self.rolls[red + yellow - 2] += 1
		self.numRolls += 1
		
	def getRolls(self):
		red = self.redDie.rolls
		yellow = self.yellowDie.rolls
		combined = self.rolls
		
		return (red, yellow, combined)
	
	def getPercentages(self, numRolls=None):
		if not numRolls:
			numRolls = self.numRolls
			
		red = [100*n/numRolls for n in self.redDie.rolls]
		yellow = [100*n/numRolls for n in self.yellowDie.rolls]
		combined = [100*n/numRolls for n in self.rolls]
		
		return (red, yellow, combined)
		
	def getAverages(self):
		red = self.redDie.getAverage()
		yellow = self.yellowDie.getAverage()
		combined = red + yellow
		
		return (red, yellow, combined)

	def displaySeparately(self):
		rTotal = 0
		yTotal = 0
		numRolls = self.numRolls if self.numRolls else 1	# Prevent dividing by 0

		string = "RED:\t\t\tYELLOW:\n"

		for i in range(6):
			rPercent = round(float(self.redDie.rolls[i]) / float(numRolls) * 100, 2)
			yPercent = round(float(self.yellowDie.rolls[i]) / float(numRolls) * 100, 2)

			string += (str(i+1) + ": " + str(self.redDie.rolls[i]) + 
				"\t" + str(rPercent) + " %" +
				"\t\t" + str(i+1) + ": " + str(self.yellowDie.rolls[i]) + 
				"\t" + str(yPercent) + " %\n")

			rTotal += (i+1) * self.redDie.rolls[i]
			yTotal += (i+1) * self.yellowDie.rolls[i]

		rAverage = round(float(rTotal) / float(numRolls), 2)
		yAverage = round(float(yTotal) / float(numRolls), 2)
		
		string += "\n"
		string += ("Average: " + str(rAverage) +
			"\t\tAverage: " + str(yAverage) + "\n")
		string += "\n"
		
		return string

	def graphResults(self, title):
		octave.histogram(self.redDie.rolls, self.yellowDie.rolls, self.rolls, title)

	def testDice(self):
		string = self.displaySeparately()
		string += self.redDie.testDie("Red")
		string += self.yellowDie.testDie("Yellow")
		return string

