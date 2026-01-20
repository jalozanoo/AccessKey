# storage/filesystem.py
import json
import os

class FileStorage:
    def __init__(self, path="vault.json"):
        self.path = path

    def save(self, salt: bytes, encrypted: bytes):
        """
        Guarda el vault cifrado y el salt en JSON
        Mantiene compatibilidad con el vault actual (UTF-8 directo)
        """
        data = {
            "salt": salt.hex(),
            "vault": encrypted.decode("utf-8")  # 🔹 mantener decode antiguo
        }

        with open(self.path, "w") as f:
            json.dump(data, f)

        # 🔐 Hardening: permisos solo para el usuario actual
        try:
            os.chmod(self.path, 0o600)
        except Exception:
            pass  # Windows u OS sin soporte

    def load(self):
        """
        Carga el vault desde JSON.
        """
        if not os.path.exists(self.path):
            return None

        with open(self.path) as f:
            data = json.load(f)

        salt = bytes.fromhex(data["salt"])
        encrypted = data["vault"].encode("utf-8")  # 🔹 mantener encode antiguo
        return salt, encrypted
