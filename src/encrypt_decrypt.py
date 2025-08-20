
---

```python
"""
encrypt_decrypt.py
Fonctions de chiffrement/déchiffrement AES-256-GCM
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, 32, count=100000, hmac_hash_module=SHA256)

def encrypt_file(data: bytes, password: str) -> bytes:
    salt = get_random_bytes(16)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return salt + cipher.nonce + tag + ciphertext

def decrypt_file(data: bytes, password: str) -> bytes:
    salt = data[:16]
    nonce = data[16:32]
    tag = data[32:48]
    ciphertext = data[48:]
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
