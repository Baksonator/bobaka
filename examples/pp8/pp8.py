counter = 0
c = 0
def reset(n):
	global counter
	global c
	return (n * 0)

def plus2(n):
	global counter
	global c
	return (n + 2)

def plus1(n):
	global counter
	global c
	return (n + 1)

def writeLn(input,size):
	global counter
	global c
	c = reset(c)
	while (c != ((size - counter) // 2)):
		print(' ', end='')
		c = plus1(c)

	while (c != (((size - counter) // 2) + counter)):
		print(input[c], end='')
		c = plus1(c)

	while (c != size):
		print(' ', end='')
		c = plus1(c)

	print(' ')

def outputEven(input,size):
	global counter
	global c
	counter = plus2(counter)
	while (counter != size):
		writeLn(input,size)
		counter = plus2(counter)

	print(input)

def outputOdd(input,size):
	global counter
	global c
	counter = plus1(counter)
	while (counter != size):
		writeLn(input,size)
		counter = plus2(counter)

	print(input)

def output(input):
	global counter
	global c
	if ((len(input) % 2) == 0):
		outputEven(input,len(input))
	else:
		outputOdd(input,len(input))

def main():
	output(input())

main()
