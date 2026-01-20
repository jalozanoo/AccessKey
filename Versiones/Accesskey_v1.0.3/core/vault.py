# core/vault.py
import json
from core.models import Credential

class Vault:
    def __init__(self):
        self._items = {}

    def add(self, credential: Credential):
        self._items[credential.name] = credential

    def list_names(self):
        return sorted(self._items.keys())

    def get(self, name):
        return self._items.get(name)

    def to_bytes(self) -> bytes:
        return json.dumps({
            k: vars(v) for k, v in self._items.items()
        }).encode()

    @staticmethod
    def from_bytes(data: bytes):
        vault = Vault()
        raw = json.loads(data.decode())
        for k, v in raw.items():
            vault._items[k] = Credential(**v)
        return vault
