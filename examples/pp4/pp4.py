z = 0
n = 0
def add(x,y):
	global z
	global n
	return (x + y)

def plus1(x):
	global z
	global n
	return (x + 1)

def mean(list):
	global z
	global n
	while (n != len(list)):
		z = add(z,int(list[n]))
		n = plus1(n)

	print((z / n))

def main():
	mean(input().split())

main()
