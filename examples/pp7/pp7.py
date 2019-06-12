brojac = 0
def plus1(x):
	global brojac
	return (x + 1)

def tarabaZvezda(ulaz):
	global brojac
	while (brojac != (len(ulaz) - 1)):
		if ulaz[brojac].isdigit():
			if ulaz[(brojac + 1)].isalpha():
				print((ulaz[brojac] + '#'), end='')
			else:
				print(ulaz[brojac], end='')
		else:
			if ulaz[brojac].isalpha():
				if ulaz[(brojac + 1)].isdigit():
					print((ulaz[brojac] + '*'), end='')
				else:
					print(ulaz[brojac], end='')
			else:
				print(ulaz[brojac], end='')
		brojac = plus1(brojac)

	print(ulaz[brojac], end='')

def main():
	tarabaZvezda(input())

main()
