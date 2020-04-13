from hashlib import sha256

from gnupg import *
import os, struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

# Obtención de SHA256 Hash para validación de contraseñas
def getHash(string):
    hashedWord = sha256(string.encode('ascii')).hexdigest()
    return hashedWord

# Cifrado y descifrado de String
mode = AES.MODE_CBC
IV = 16 * '\x00'


def cifrar(key, text):
    # Obtenemos los 32 primeros dígitos del hash como clave
    key = key[32:]
    # Transformamos el texto a cifrar para hacerlo múltiplo de 16
    text = (text + '\n') * 16
    encryptor = AES.new(key, mode, IV=IV)
    return encryptor.encrypt(text)


def descifrar(key, crypted):
    key = key[32:]
    decryptor = AES.new(key, mode, IV=IV)
    return decryptor.decrypt(crypted).splitlines()[0].decode('ascii')
