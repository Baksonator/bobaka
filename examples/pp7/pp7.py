counter = 0
def plus1(x):
	global counter
	return (x + 1)

def hashtagAsterisk(input):
	global counter
	while (counter != (len(input) - 1)):
		if input[counter].isdigit():
			if input[(counter + 1)].isalpha():
				print((input[counter] + '#'), end='')
			else:
				print(input[counter], end='')
		else:
			if input[counter].isalpha():
				if input[(counter + 1)].isdigit():
					print((input[counter] + '*'), end='')
				else:
					print(input[counter], end='')
			else:
				print(input[counter], end='')
		counter = plus1(counter)

	print(input[counter], end='')

def main():
	hashtagAsterisk(input())

main()
