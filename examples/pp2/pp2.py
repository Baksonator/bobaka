z = 0
def isZero(n):
	global z
	return (n == 0)

def division10(n):
	global z
	return (n // 10)

def addMod10(x,y):
	global z
	return (x + (y % 10))

def greaterThanTen(n):
	global z
	if (n > 10):
		print('Greater')
	else:
		print('Less')


main()
