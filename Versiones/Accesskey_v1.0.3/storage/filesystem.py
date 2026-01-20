# storage/filesystem.py
import json, os

class FileStorage:
    def __init__(self, path="vault.json"):
        self.path = path

    def save(self, salt: bytes, encrypted: bytes):
        with open(self.path, "w") as f:
            json.dump({
                "salt": salt.hex(),
                "vault": encrypted.decode()
            }, f)

    def load(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path) as f:
            data = json.load(f)
            return bytes.fromhex(data["salt"]), data["vault"].encode()