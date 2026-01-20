#AccessKey v1.0
#Program to give or save keys needed to acces to several platforms
#Created by Jhonatan Lozano

from give import *
from save import *
from crypto import *
from parse import *
import json

D = {}

def load_Dictionary():
    count = 0
    password = []
    f = open("passwords.txt", "r")
    for x in f:
        password.append(x)
        key_msm = parse("{key}|{msm}\n", password[count])

        #Generate Fernet uncryption
        msm_cryp = crypto(key_msm['key'].encode(),None,key_msm['msm'].encode(),False)

        #Updating dictionary
        D_item = json.loads(msm_cryp.decode())
        D.update(D_item)

        count = count+1
    password.clear()
    f.close()

def acceskey_menu():
    print("Seleccione una opción\n")
    print("1. Guardar nuevo acceso.\n")
    print("2. Solicitar información de acceso.\n")
    print("3. Salir.\n")
    opt = int(input())
    return opt

while 1:
    opt = acceskey_menu()
    if opt == 1:
        save()
        print("Nuevo acceso almacenado exitosamente.\n")
    elif opt == 2:
        load_Dictionary()
        give(D)
        D.clear()
    elif opt == 3:
        D.clear()
        quit()
    else:
        print("Ingrese 1, 2 o 3")

