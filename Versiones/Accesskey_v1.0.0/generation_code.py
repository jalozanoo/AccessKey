#Extension to generate a new password. Used from https://geekflare.com/es/password-generator-python-code/
import string
import random

characters = list(string.ascii_letters + string.digits + "!#$%&")

def generate_random_password():

	length = int(input("Logitud de la contraseña: "))

	random.shuffle(characters)
	
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	random.shuffle(password)

	return"".join(password)



