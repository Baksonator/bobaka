import random
counter = 0
def plus1(x):
	global counter
	return (x + 1)

def randomNumbers(n):
	global counter
	while (counter != n):
		print(random.randrange(1,101))
		counter = plus1(counter)

	return counter

def main():
	randomNumbers(int(input()))

main()
