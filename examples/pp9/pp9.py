counter = 0
prev = 0
res = False
def setTrue():
	global counter
	global prev
	global res
	return True

def setFalse():
	global counter
	global prev
	global res
	return False

def longerThanN(input,n):
	global counter
	global prev
	global res
	if (len(input) > n):
		res = setTrue()
	else:
		res = setFalse()
	return res

def plus1(n):
	global counter
	global prev
	global res
	return (n + 1)

def returnCounter():
	global counter
	global prev
	global res
	return counter

def solveOne(input,size,n):
	global counter
	global prev
	global res
	while (counter < size) and (input[counter] != ',') and (input[counter] != '.') and (input[counter] != '!') and (input[counter] != '?') and (input[counter] != ' '):
		(1 + 2)
		counter = plus1(counter)

	if longerThanN(input[prev:counter],n):
		print(input[prev:counter].upper())
	else:
		print(input[prev:counter])
	counter = plus1(counter)
	prev = returnCounter()

def solveAll(input,n):
	global counter
	global prev
	global res
	while (counter < len(input)):
		solveOne(input,len(input),n)


def main():
	solveAll(input(),int(input()))

main()
