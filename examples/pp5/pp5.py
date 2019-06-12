import random
brojac = 0
def plus1(x):
	global brojac
	return (x + 1)

def nasumicniBrojevi(n):
	global brojac
	while (brojac != n):
		print(random.randrange(1,101))
		brojac = plus1(brojac)

	return brojac

def main():
	nasumicniBrojevi(int(input()))

main()
