# core/models.py
from dataclasses import dataclass

@dataclass
class Credential:
    name: str
    username: str
    password: str
    correo: str = ""