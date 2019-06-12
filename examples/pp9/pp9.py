brojac = 0
prev = 0
res = False
def setTrue():
	global brojac
	global prev
	global res
	return True

def setFalse():
	global brojac
	global prev
	global res
	return False

def duzaN(ulaz,n):
	global brojac
	global prev
	global res
	if (len(ulaz) > n):
		res = setTrue()
	else:
		res = setFalse()
	return res

def plus1(n):
	global brojac
	global prev
	global res
	return (n + 1)

def vratiBrojac():
	global brojac
	global prev
	global res
	return brojac

def resiJedna(ulaz,size,n):
	global brojac
	global prev
	global res
	while (brojac < size) and (ulaz[brojac] != ',') and (ulaz[brojac] != '.') and (ulaz[brojac] != '!') and (ulaz[brojac] != '?') and (ulaz[brojac] != ' '):
		(1 + 2)
		brojac = plus1(brojac)

	if duzaN(ulaz[prev:brojac],n):
		print(ulaz[prev:brojac].upper())
	else:
		print(ulaz[prev:brojac])
	brojac = plus1(brojac)
	prev = vratiBrojac()

def resiSve(ulaz,n):
	global brojac
	global prev
	global res
	while (brojac < len(ulaz)):
		resiJedna(ulaz,len(ulaz),n)


def main():
	resiSve(input(),int(input()))

main()
