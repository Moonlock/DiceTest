#include <string>
#include <iostream>
#include <utility>
#include <cmath>
using namespace std;

typedef struct DIE
{
	int rolls[6];
	string name;

	DIE(string name)
	 : rolls{0,0,0,0,0,0},
	   name(name)
	{}

	double getChiSquare(int numRolls)
	{
		double expected = numRolls/6;

		double chiSquare = 0;
		for(int i = 0; i < 6; i++)
		{
			chiSquare += pow(rolls[i] - expected, 2) / expected;
		}

		return chiSquare;
	}

	void display(int numRolls)
	{
		cout << "\n" << name << ":\n";
		for(int i=0; i<6; i++)
		{
			cout << i+1 << ": " << rolls[i] << '\t' <<
					(double)rolls[i] / (double)numRolls * 100 <<
					endl;
		}
	}
} Die;

class Dice
{
public:
	Dice();

	void addRolls(string roll1, string roll2);

	void testDice();

	void displaySeparately();

	void displayCombined();

private:
	void testDie(Die die);

private:
	Die die1, die2;
	int rolls[11];
	int numRolls;
};