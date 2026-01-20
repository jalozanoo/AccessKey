# core/auth.py
import os
from core.crypto import CryptoManager

class AuthManager:
    def __init__(self, storage):
        self.storage = storage

    def first_time_setup(self):
        password = input("Crea una contraseña maestra: ")
        salt = os.urandom(16)
        crypto = CryptoManager(password, salt)
        return crypto, salt

    def login(self):
        data = self.storage.load()
        if data is None:
            return None, None, None

        salt, encrypted_vault = data

        for _ in range(3):
            password = input("Ingrese contraseña maestra: ")
            try:
                crypto = CryptoManager(password, salt)
                vault_data = crypto.decrypt(encrypted_vault)
                return crypto, salt, vault_data
            except Exception:
                print("Contraseña incorrecta.\n")

        print("Demasiados intentos.")
        exit()

    def change_master_password(self, old_crypto, vault):
        print("\n=== Cambio de contraseña maestra ===")
        new_password = input("Nueva contraseña maestra: ")
        confirm = input("Confirmar nueva contraseña: ")

        if new_password != confirm:
            print("Las contraseñas no coinciden.")
            return None, None

        new_salt = os.urandom(16)
        new_crypto = CryptoManager(new_password, new_salt)

        return new_crypto, new_salt
