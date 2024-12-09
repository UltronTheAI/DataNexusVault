from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import random
import string
import os

def generate_random_key(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation  # a-z, A-Z, 0-9, symbols
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt_data(key, plaintext):
    # Derive a 256-bit AES key from the password
    salt = os.urandom(16)  # 16-byte random salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    aes_key = kdf.derive(key.encode('utf-8'))

    # Generate a random nonce (12 bytes for AES-GCM)
    nonce = os.urandom(12)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()

    # Return salt, nonce, and ciphertext
    return salt + nonce + ciphertext + encryptor.tag

def decrypt_data(key, encrypted_data):
    # Extract salt, nonce, and ciphertext
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[28:-16]

    # Derive the same AES key using the salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    aes_key = kdf.derive(key.encode('utf-8'))

    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode('utf-8')

"""
if __name__ == "__main__":
    key = generate_random_key()
    data = ""

    encrypted = encrypt_data(key, data)
    print("Encrypted:", encrypted.hex())

    decrypted = decrypt_data(key, encrypted)
    print("Decrypted:", decrypted)
"""