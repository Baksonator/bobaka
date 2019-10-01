import math
z = 0
listOf = []
counter = 0
root = 0
res = False
def readUntil():
	global z
	global listOf
	global counter
	global root
	global res
	z = int(input())
	while (z > 0):
		listOf.append(z)
		z = int(input())


def setTrue():
	global z
	global listOf
	global counter
	global root
	global res
	return True

def setFalse():
	global z
	global listOf
	global counter
	global root
	global res
	return False

def checkNumber(n):
	global z
	global listOf
	global counter
	global root
	global res
	root = round(math.sqrt(n))
	if ((root * root) == n):
		res = setTrue()
	else:
		res = setFalse()
	return res

def plus1(x):
	global z
	global listOf
	global counter
	global root
	global res
	return (x + 1)

def outputNumbers(size):
	global z
	global listOf
	global counter
	global root
	global res
	if checkNumber(listOf[counter]):
		print(listOf[counter], end='')
	else:
		(2 + 3)
	counter = plus1(counter)
	while (counter != size):
		if checkNumber(listOf[counter]):
			print((',' + str(listOf[counter])), end='')
		else:
			1
		counter = plus1(counter)


def solve():
	global z
	global listOf
	global counter
	global root
	global res
	readUntil()
	outputNumbers(len(listOf))

def main():
	solve()

main()
