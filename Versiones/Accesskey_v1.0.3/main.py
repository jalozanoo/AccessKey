
# main.py
from storage.filesystem import FileStorage
from core.auth import AuthManager
from core.vault import Vault
from ui.cli import main_menu, create_credential, show_credentials

storage = FileStorage()
auth = AuthManager(storage)

loaded = storage.load()

if loaded is None:
    print("=== Configuración inicial ===")
    crypto, salt = auth.first_time_setup()
    vault = Vault()
else:
    crypto, salt, vault_bytes = auth.login()
    vault = Vault.from_bytes(vault_bytes)

while True:
    opt = main_menu()

    if opt == "1":
        cred = create_credential()
        if cred:
            vault.add(cred)

    elif opt == "2":
        show_credentials(vault)

    elif opt == "3":
        result = auth.change_master_password(crypto, vault)
        if result != (None, None):
            crypto, salt = result
            print("Contraseña maestra cambiada correctamente.")

    elif opt == "4":
        storage.save(salt, crypto.encrypt(vault.to_bytes()))
        print("Datos guardados. Saliendo.")
        break

    else:
        print("Opción inválida.")