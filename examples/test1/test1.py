brojac = 0
sadrzaj = 0
pokazivac = 0
pokazivac2 = 0
pomocna = 0
def plus1(n):
	global brojac
	global sadrzaj
	global pokazivac
	global pokazivac2
	global pomocna
	return (n + 1)

def reset(n):
	global brojac
	global sadrzaj
	global pokazivac
	global pokazivac2
	global pomocna
	return (n * 0)

def jednaRec(rec):
	global brojac
	global sadrzaj
	global pokazivac
	global pokazivac2
	global pomocna
	brojac = reset(brojac)
	pokazivac = reset(pokazivac)
	pomocna = sadrzaj.split()
	while (pokazivac != len(pomocna)):
		if (pomocna[pokazivac].lower() == rec):
			brojac = plus1(brojac)
		else:
			1
		pokazivac = plus1(pokazivac)

	print(rec,brojac)

def resi(fajl,broj,reci):
	global brojac
	global sadrzaj
	global pokazivac
	global pokazivac2
	global pomocna
	praveReci = reci.split()
	sadrzaj = open(fajl, "r").read()
	while (pokazivac2 != broj):
		jednaRec(praveReci[pokazivac2])
		pokazivac2 = plus1(pokazivac2)


def main():
	resi(input(),int(input()),input())

main()
