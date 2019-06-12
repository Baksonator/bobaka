brojac = 0
c = 0
def reset(n):
	global brojac
	global c
	return (n * 0)

def plus2(n):
	global brojac
	global c
	return (n + 2)

def plus1(n):
	global brojac
	global c
	return (n + 1)

def ispisReda(ulaz,size):
	global brojac
	global c
	c = reset(c)
	while (c != ((size - brojac) // 2)):
		print(' ', end='')
		c = plus1(c)

	while (c != (((size - brojac) // 2) + brojac)):
		print(ulaz[c], end='')
		c = plus1(c)

	while (c != size):
		print(' ', end='')
		c = plus1(c)

	print(' ')

def ispisParno(ulaz,size):
	global brojac
	global c
	brojac = plus2(brojac)
	while (brojac != size):
		ispisReda(ulaz,size)
		brojac = plus2(brojac)

	print(ulaz)

def ispisNeparno(ulaz,size):
	global brojac
	global c
	brojac = plus1(brojac)
	while (brojac != size):
		ispisReda(ulaz,size)
		brojac = plus2(brojac)

	print(ulaz)

def ispis(ulaz):
	global brojac
	global c
	if ((len(ulaz) % 2) == 0):
		ispisParno(ulaz,len(ulaz))
	else:
		ispisNeparno(ulaz,len(ulaz))

def main():
	ispis(input())

main()
