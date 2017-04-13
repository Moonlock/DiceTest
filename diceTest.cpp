#include "diceTest.h"
using namespace std;

pair<double, double> getPValue(double chiSquare)
{
	if(chiSquare <= 1.61)
		return make_pair(0.90, 1);
	if(chiSquare <= 2.675)
		return make_pair(0.75, 0.9);
	if(chiSquare <= 4.351)
		return make_pair(0.50, 0.75);
	if(chiSquare <= 6.626)
		return make_pair(0.25, 0.5);
	if(chiSquare <= 9.236)
		return make_pair(0.1, 0.25);
	if(chiSquare <= 11.07)
		return make_pair(0.05, 0.1);
	if(chiSquare <= 12.83)
		return make_pair(0.025, 0.05);
	if(chiSquare <= 15.086)
		return make_pair(0.01, 0.025);

	return make_pair(0, 0.01);
}

Dice::Dice()
	: die1("RED"),
	  die2("YELLOW"),
	  rolls{0,0,0,0,0,0,0,0,0,0,0},
	  numRolls(0)
{}

void Dice::addRolls(string roll1, string roll2)
{
	int val1 = stoi(roll1);
	int val2 = stoi(roll2);

	die1.rolls[val1-1]++;
	die2.rolls[val2-1]++;
	rolls[val1 + val2 - 2]++;

	numRolls++;
}

void Dice::testDice()
{
	testDie(die1);
	testDie(die2);
}

void Dice::testDie(Die die)
{
	die.display(numRolls);
	pair<double, double> pValue = getPValue(die.getChiSquare(numRolls));
	if(pValue.second <= 0.05)
	{
		cout << "Die is rigged.  ";
	}
	else
	{
		cout << "Die is not rigged.  ";
	}
	cout << "( " << pValue.first << " > p > " << pValue.second << " )\n";
}

void Dice::displaySeparately()
{
	die1.display(numRolls);
	die2.display(numRolls);
	cout << endl;
}

void Dice::displayCombined()
{
	cout << endl;
	for(int i=0; i<11; i++)
	{
		cout << i+2 << ": " << rolls[i] << '\t' <<
				(double)rolls[i] / (double)numRolls * 100 <<
				endl;
	}
	cout << endl;
}

int main(int argc, char** argv)
{
	string red, yellow;
	Dice* dice = new Dice();

	cout << "\nEnter dice: (Red then yellow)\n";
	cout << "'d' to display dice separately, 'q' to quit.\n\n";
	while(true)
	{
		cout << "R Y: ";

		cin >> red;
		if(red == "q")
			break;
		if(red == "d")
		{
			dice->displaySeparately();
			continue;
		}
		cin >> yellow;

		dice->addRolls(red, yellow);
		dice->displayCombined();
	}

	dice->testDice();
	return 0;
}
