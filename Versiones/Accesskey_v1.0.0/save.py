#Extension to save a new key
from generation_code import *
from crypto import *
import json
import os

def get_password():
    flag = input("¿Desea que se genere una contraseña? (s/n)")
    if flag == "s" or flag == "n":
        if flag == "s":
            code = generate_random_password()
        else:
            code = input("Ingrese contraseña: ")
    else:
        os.system("cls")
        print("Seleccione una opción valida.\n")
        return -1
    return code

def save():
    os.system("cls")
    flag = False
    #To catch the password by generating it or as input
    while 1:
        opt = input("¿Desea guardar un usuario y contraseña? (s/n)")
        if opt == "n":
            program = input("Nombre del acceso: ")
            code = get_password() 
            if code != -1: break
        elif opt == "s":
            flag = True
            program = input("Nombre del acceso: ")
            user = input("Ingrese el usuario: ")
            code = get_password() 
            if code != -1: break
        else:
            os.system("cls")
            print("Seleccione una opción valida.\n")
            continue

    #Generate Dictionary
    if flag == False:
        D = {program:code}
    elif flag == True:
        D = {program:user+"/"+code}
    else:
        print("Fatal error. Closing AccessKey...")
        quit()
    
    D_str = json.dumps(D).encode('utf-8')

    #Generate Fernet encryption
    key = Fernet.generate_key()
    msm_cryp = crypto(key,D_str,None,True)

    #Updating text file
    f = open("passwords.txt", "a")
    f.write(key.decode()+"|"+msm_cryp.decode()+"\n")
    f.close()