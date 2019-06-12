z = 0
n = 0
def saberi(x,y):
	global z
	global n
	return (x + y)

def plus1(x):
	global z
	global n
	return (x + 1)

def arithmSredina(lista):
	global z
	global n
	while (n != len(lista)):
		z = saberi(z,int(lista[n]))
		n = plus1(n)

	print((z / n))

def main():
	arithmSredina(input().split())

main()
