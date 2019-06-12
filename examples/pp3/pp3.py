def maksimumOd4(x,y,z,t):
	if (x > y):
		if (x > z):
			if (x > t):
				print(x)
			else:
				print(t)
		else:
			if (z > t):
				print(z)
			else:
				print(t)
	else:
		if (y > z):
			if (y > t):
				print(y)
			else:
				print(t)
		else:
			if (z > t):
				print(z)
			else:
				print(t)

def main():
	maksimumOd4(int(input()),int(input()),int(input()),int(input()))

main()
