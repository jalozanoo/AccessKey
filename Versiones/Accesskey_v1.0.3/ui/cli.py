# ui/cli.py
from core.models import Credential
from utils.password_gen import generate_password

def main_menu():
    print("\nSeleccione una opción:")
    print("1. Guardar nuevo acceso")
    print("2. Mostrar accesos")
    print("3. Cambiar contraseña maestra")
    print("4. Salir")

    return input("> ")

def create_credential():
    name = input("Nombre del acceso: ")
    username = input("Usuario (opcional): ")

    opt = input("¿Generar contraseña automáticamente? (s/n): ")
    if opt.lower() == "s":
        password = generate_password()
        print("Contraseña generada:", password)
    else:
        password = input("Ingrese contraseña: ")

    confirm = input("¿Confirmar guardado? (s/n): ")
    if confirm.lower() != "s":
        return None

    return Credential(name, username, password)

def show_credentials(vault):
    names = vault.list_names()
    if not names:
        print("No hay accesos almacenados.\n")
        return

    print("\nAccesos guardados:")
    for n in names:
        print("-", n)

    key = input("\nSeleccione uno (o B para volver): ")
    if key.lower() == "b":
        return

    cred = vault.get(key)
    if cred:
        print("\nUsuario:", cred.username)
        print("Contraseña:", cred.password)
    else:
        print("Acceso no encontrado.")
