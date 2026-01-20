import os
import time
import hashlib
from parse import *
from generation_code import *

def start():
    os.system("cls")
    print("Bienvenido a AccessKey, tu gestionador de contraseñas.\n")
    print("\n AVISO IMPORTANTE\n")
    print("Para garantizar la seguridad de tus contraseñas deberás ingresar una contraseña única la cual deberás proteger.\n")
    print("Esta contraseña será la única que NO será gestionada por AccessKey y deberá ser protegida por tí.\n")
    print("Se te solicitará ingresar esta contraseña cada vez que quieras acceder a tus contraseñas. Esta estará totalmente protegida.\n")
    print("Para modificar esta contraseña deberás ingresar su versión actual. Es importante que la protejas.\n")
    print("")
    
    while(1):
        user_input = input("¿Desea continuar? (s/n)\n")
        if (user_input == "S" or user_input == "s"):
            while 1:
                user_input = input("\nCrea una nueva clave: ") 
                if bool(user_input) == False:
                    os.system("cls")
                    error_msm(4)
                    continue
                else:
                    return user_input
        elif (user_input == "N" or user_input == "n"):
            print("Es una lástima, nos veremos en otra ocasión.\n")
            quit()
        else:
            os.system("cls")
            error_msm(4)
    
def succes():
    os.system("cls")
    print("Ha creado su contraseña con exito. No olvide almacenarla en un lugar seguro.\n")
    time.sleep(3)

def menu_general():
    os.system("cls")
    print("Seleccione una opción\n")
    print("1. Guardar nuevo acceso.\n")
    print("2. Solicitar información de acceso.\n")
    print("3. Cambiar contraseña de inicio.\n")
    print("4. Salir y guardar de forma segura.\n")

def input_password(key):
    os.system("cls")
    counter = 0;
    while 1:
        user_input = input("Ingrese clave para empezar: ") 
        if bool(user_input) == False:
            error_msm(2)
            continue
        else:
            if hashlib.sha256(user_input.encode()).hexdigest() == key:
                return True
            else:
                error_msm(2)
                counter += 1
                if(counter >=3):
                    error_msm(3)
                    return False

def not_succes(msm):
    os.system("cls")
    print(msm,"\n")
    time.sleep(2)

def confirmation_alert(msm):
    os.system("cls")
    print('Se creará el acceso \'{}\' con usuario {} y contraseña {}.'.format(msm[0],msm[1],msm[2]))
    return input('\n ¿Desea confirmar? (s/n) ')
    
def get_password():
    opt = input("¿Desea que se genere una contraseña? (s/n) ")
    if opt == "s" or opt == "n" or opt == "S" or opt == "N":
        if opt == "s" or opt == "S":
            code = generate_random_password()
        else:
            code = input("Ingrese contraseña: ")
    else:
        os.system("cls")
        error_msm(4)
        return -1
    return code

def data_to_save():
    while 1:
        os.system("cls")
        print("\nPresione B para volver. Si confirma proceso deberá completarlo.\n")
        opt = input("¿Desea guardar un usuario y contraseña? (s/n) ")
        if opt == "n" or opt == "N":
            os.system("cls")
            program = input("Nombre del acceso: ")
            user = "Not user";
            code = get_password() 
            if code != -1 and confirmation_alert([program,'no especificado','\''+code+'\'']) == "s": 
                return [program,user,code,False]
        elif opt == "s" or opt == "S":
            os.system("cls")
            program = input("Nombre del acceso: ")
            user = input("Ingrese el usuario: ")
            code = get_password() 
            if code != -1 and confirmation_alert([program,'\''+user+'\'','\''+code+'\'']) == "s": 
                return [program,user,code, True]
        elif opt == "b" or opt == "B":
            return -1
        else:
            os.system("cls")
            error_msm(4)
            continue

def print_sorted_list(D_list, D, columns):
    os.system("cls")
    D_list.sort()
    
    if len(D_list) == 0:
        print('No tiene ningun acceso almacenado.\n')
    else:
        while True:
            print("Tiene accesos a estas instancias: \n")
            
            max_length = max(len(item) for item in D_list)
            column_width = max_length + 4
            
            for i in range(len(D_list)):
                print(f"{D_list[i]:<{column_width}}", end="")
                if (i + 1) % columns == 0:
                    print()
            if (i + 1) % columns != 0:
                print()
            print()
            print("\nPara volver presione B.\n")
            key = input("Seleccione una de las anteriores opciones -> ")
            
            if key in D:
                os.system("cls")
                user_key = parse("{user}/{key}/{flag}", D[key])
                if "True" in str(D[key]): 
                    print("\n El acceso a "+key+" es -> Usuario: "+user_key['user']+" Contraseña: "+user_key['key']+'\n')
                else:
                    print("\n La contraseña del acceso a "+key+" es: "+user_key['key']+'\n')  
                D_list.clear()
                D.clear()
                break
            elif key == "B" or key == "b":
                break
            else:
                os.system("cls")
                error_msm(4)
                time.sleep(3)

def error_msm(num):
    if num == 1:
        print('Error durante encripción. Cerrando AccessKey.\n')
    elif num == 2:
        print('Error de contraseña. Intente de nuevo.\n')
    elif num == 3:
            os.system("cls")
            print('Ha alcanzado el número de intentos máximo permitidos. Comuniquese con nuestro centro de servicios para cambiar la contraseña.\n')
    elif num == 4:
        print("Ingrese una opción valida.\n")
    elif num == 5:
         print('Error al iniciar. Cerrando AccessKey.\n')

def warning_msm(num):
    if num == 1:
        while(1):
            os.system("cls")
            opt = input('Al cambiar la contraseña se eliminará por completo la contraseña actual. ¿Quiere continuar? s/n.\n')
            if opt == "s" or opt == "S":
                return True
            elif opt == "n" or opt == "N":
                return False
            else:
                error_msm(4)
                time.sleep(3)

