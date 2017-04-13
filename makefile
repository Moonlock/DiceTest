CC = g++
CFLAGS = -g -Wall -pedantic

all: diceTest

diceTest: diceTest.o
	$(CC) $(CFLAGS) diceTest.o -o diceTest

diceTest.o: diceTest.h diceTest.cpp
	$(CC) $(CFLAGS) -c diceTest.cpp

clean:
	rm -rf *.o diceTest

.PHONY: all clean
