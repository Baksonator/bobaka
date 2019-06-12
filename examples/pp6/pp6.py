import math
z = 0
lista = []
brojac = 0
koren = 0
res = False
def ucitavanjeDok():
	global z
	global lista
	global brojac
	global koren
	global res
	z = int(input())
	while (z > 0):
		lista.append(z)
		z = int(input())


def setTrue():
	global z
	global lista
	global brojac
	global koren
	global res
	return True

def setFalse():
	global z
	global lista
	global brojac
	global koren
	global res
	return False

def proveriBroj(n):
	global z
	global lista
	global brojac
	global koren
	global res
	koren = round(math.sqrt(n))
	if ((koren * koren) == n):
		res = setTrue()
	else:
		res = setFalse()
	return res

def plus1(x):
	global z
	global lista
	global brojac
	global koren
	global res
	return (x + 1)

def ispisiBrojeve(size):
	global z
	global lista
	global brojac
	global koren
	global res
	if proveriBroj(lista[brojac]):
		print(lista[brojac], end='')
	else:
		(2 + 3)
	brojac = plus1(brojac)
	while (brojac != size):
		if proveriBroj(lista[brojac]):
			print((',' + str(lista[brojac])), end='')
		else:
			1
		brojac = plus1(brojac)


def resi():
	global z
	global lista
	global brojac
	global koren
	global res
	ucitavanjeDok()
	ispisiBrojeve(len(lista))

def main():
	resi()

main()
