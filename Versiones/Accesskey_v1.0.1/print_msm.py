import os
import time
import hashlib
from parse import *
from generation_code import *

def start():
    os.system("cls")
    print("Bienvenido a AccessKey, tu gestionador de contraseñas.\n")
    print("Se te solicitará una clave cada vez que necesites gestionar algun acceso.\n")
    while 1:
        user_input = input("Crea una nueva clave: ") 
        if bool(user_input) == False:
            print("Ingrese una clave no vacía.\n")
            continue
        else:
            return user_input

def input_password(key):
    os.system("cls")
    while 1:
        user_input = input("Ingrese clave para empezar: ") 
        if bool(user_input) == False:
            print("Ingrese una clave no vacía.\n")
            continue
        else:
            if hashlib.sha256(user_input.encode()).hexdigest() == key:
                return True
            else:
                print('La clave es incorrecta. Vuelva a intentar.\n')
                continue

def succes():
    os.system("cls")
    print("Operación exitosa.\n")
    time.sleep(2)

def not_succes(msm):
    os.system("cls")
    print(msm,"\n")
    time.sleep(2)

def menu_general():
    os.system("cls")
    print("Seleccione una opción\n")
    print("1. Guardar nuevo acceso.\n")
    print("2. Solicitar información de acceso.\n")
    print("3. Salir y guardar de forma segura.\n")

def confirmation_alert(msm):
    os.system("cls")
    print('Se creará el acceso \'{}\' con usuario {} y contraseña {}.'.format(msm[0],msm[1],msm[2]))
    return input('\n ¿Desea confirmar? (s/n) ')
    
def get_password():
    flag = input("¿Desea que se genere una contraseña? (s/n) ")
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

def data_to_save():
    while 1:
        os.system("cls")
        opt = input("¿Desea guardar un usuario y contraseña? (s/n) ")
        if opt == "n":
            program = input("Nombre del acceso: ")
            code = get_password() 
            if code != -1 and confirmation_alert([program,'no especificado','\''+code+'\'']) == "s": 
                return [program,'Not user',code,False]
        elif opt == "s":
            program = input("Nombre del acceso: ")
            user = input("Ingrese el usuario: ")
            code = get_password() 
            if code != -1 and confirmation_alert([program,'\''+user+'\'','\''+code+'\'']) == "s": 
                return [program,user,code, True]
        else:
            os.system("cls")
            print("Seleccione una opción valida.\n")
            continue

def print_sorted_list(D_list, D, columns):
    os.system("cls")
    D_list.sort()
    x = columns
    if len(D_list) == 0:
        print('No tiene ningun acceso almacenado.\n')
    else:
        print("Tiene accesos de estas instancias: \n")
        for i in range(len(D_list)):
            print("{:<11}".format(D_list[i]), end="        ")
            if (i+1) % x == 0:
                print()
        if i != len(D_list) - 1:
            print()
        print()
        while 1:
            key = input("\nSeleccione una de las anteriores opciones -> ")
            if key in D:
                user_key = parse("{user}/{key}/{flag}",D[key])
                if "True" in str(D[key]): 
                    print("\n El acceso a "+key+" es -> Usuario: "+user_key['user']+" Contraseña: "+user_key['key']+'\n')
                else:
                    print("\n La contraseña del acceso a "+key+" es: "+user_key['key']+'\n')  
                D_list.clear()
                D.clear()
                break
            else:
                print("Seleccione una opción válida.\n")



