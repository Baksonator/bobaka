z = 0
def isNula(n):
	global z
	return (n == 0)

def deljenje10(n):
	global z
	return (n // 10)

def saberiMod10(x,y):
	global z
	return (x + (y % 10))

def veceOdDeset(n):
	global z
	if (n > 10):
		print('Vece')
	else:
		print('Manje')

def proveri(n):
	global z
	while not isNula(n):
		z = saberiMod10(z,n)
		n = deljenje10(n)

	veceOdDeset(z)

def main():
	proveri(int(input()))

main()
