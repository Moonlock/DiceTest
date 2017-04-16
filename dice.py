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

	def __init__(self, name):
		self.rolls = [0, 0, 0, 0, 0, 0]
		self.name = name
		self.numRolls = 0

	def getChiSquare(self):
		self.numRolls = self.numRolls if self.numRolls else 1	# Prevent dividing by 0

		expected = float(self.numRolls) / 6.0

		chiSquare = 0.0
		for i in range(6):
			chiSquare += pow(self.rolls[i] - expected, 2) / expected

		return chiSquare

	def addRoll(self, roll):
		self.rolls[roll-1] += 1
		self.numRolls += 1

	def testDie(self):
		pValue = getPValue(self.getChiSquare())
		if pValue[1] <= 0.05:
			print(self.name + " - Die seems to be rigged.  " +
				"( " + str(pValue[0]) + " > p > " + str(pValue[1]) + " )")
		else:
			print(self.name + " - Die does not seem to be rigged.  " +
				"( " + str(pValue[0]) + " > p > " + str(pValue[1]) + " )")

	def toDict(self):
		return {'name': self.name, 'rolls': self.rolls}


class DiceSet:

	def __init__(self):
		self.redDie = Die("RED")
		self.yellowDie = Die("YELLOW")
		self.rolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.numRolls = 0

	def addRoll(self, red, yellow):
		self.redDie.addRoll(red)
		self.yellowDie.addRoll(yellow)

		self.rolls[red + yellow - 2] += 1
		self.numRolls += 1

	def displayCombined(self):
		total = 0
		self.numRolls = self.numRolls if self.numRolls else 1	# Prevent dividing by 0

		print("")
		for i in range(11):
			percent = float(self.rolls[i]) / float(self.numRolls) * 100
			percent = round(percent, 2)

			print(str(i+2) + ": " + str(self.rolls[i]) + 
				"\t" + str(percent) + " %")
			total += (i+2) * self.rolls[i]

		average = round(float(total) / float(self.numRolls), 2)
		print("")
		print("Average: " + str(average))
		print("")

	def displaySeparately(self):
		rTotal = 0
		yTotal = 0
		self.numRolls = self.numRolls if self.numRolls else 1	# Prevent dividing by 0

		print("")
		print("    " + self.redDie.name + "\t\t\t    " + self.yellowDie.name)

		for i in range(6):
			rPercent = round(float(self.redDie.rolls[i]) / float(self.numRolls) * 100, 2)
			yPercent = round(float(self.yellowDie.rolls[i]) / float(self.numRolls) * 100, 2)

			print(str(i+1) + ": " + str(self.redDie.rolls[i]) + 
				"\t" + str(rPercent) + " %" +
				"\t\t" + str(i+1) + ": " + str(self.yellowDie.rolls[i]) + 
				"\t" + str(yPercent) + " %")

			rTotal += (i+1) * self.redDie.rolls[i]
			yTotal += (i+1) * self.yellowDie.rolls[i]

		rAverage = round(float(rTotal) / float(self.numRolls), 2)
		yAverage = round(float(yTotal) / float(self.numRolls), 2)
		print("")
		print("Average: " + str(rAverage) +
			"\t\tAverage: " + str(yAverage))
		print("")

	def graphResults(self, title):
		octave.histogram(self.redDie.rolls, self.yellowDie.rolls, self.rolls, title)

	def testDice(self):
		print("")
		self.displaySeparately()
		self.redDie.testDie()
		self.yellowDie.testDie()

	def toDict(self):
		return {'rolls': self.rolls,
			'redDie': self.redDie.toDict(), 'yellowDie': self.yellowDie.toDict()}
