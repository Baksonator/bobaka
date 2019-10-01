counter = 0
contents = 0
pointer = 0
pointer2 = 0
helper = 0
def plus1(n):
	global counter
	global contents
	global pointer
	global pointer2
	global helper
	return (n + 1)

def reset(n):
	global counter
	global contents
	global pointer
	global pointer2
	global helper
	return (n * 0)

def oneWord(word):
	global counter
	global contents
	global pointer
	global pointer2
	global helper
	counter = reset(counter)
	pointer = reset(pointer)
	helper = contents.split()
	while (pointer != len(helper)):
		if (helper[pointer].lower() == word):
			counter = plus1(counter)
		else:
			1
		pointer = plus1(pointer)

	print(word,counter)

def solve(file,number,words):
	global counter
	global contents
	global pointer
	global pointer2
	global helper
	praveReci = words.split()
	contents = open(file, "r").read()
	while (pointer2 != number):
		oneWord(praveReci[pointer2])
		pointer2 = plus1(pointer2)


def main():
	solve(input(),int(input()),input())

main()
