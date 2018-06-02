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


def cryptInfo(key, text):
    # Obtenemos los 32 primeros dígitos del hash como clave
    key = key[32:]
    # Transformamos el texto a cifrar para hacerlo múltiplo de 16
    text = (text + '\n') * 16
    encryptor = AES.new(key, mode, IV=IV)
    return encryptor.encrypt(text)


def decryptInfo(key, crypted):
    key = key[32:]
    decryptor = AES.new(key, mode, IV=IV)
    return decryptor.decrypt(crypted).splitlines()[0].decode('ascii')


def cifrar(clave, fichero):
    '''Cifra un fichero con AES.
       @param clave: la clave de cifrado
       @param fichero: el fichero a cifrar
    '''
    # Genera un hash de la clave introducida
    clave = get_clave(clave)
    # Tamaño del bloque a leer
    bs = 1024
    # Añade la extensión 'enc' al nombre del fichero de salida
    ficheroSalida = fichero
    modo_aes = AES.MODE_CBC
    # El tamaño del vector de inicialización en bytes.
    # Para el modo AES CBC tiene que ser del mismo tamaño
    # que el tamaño de bloque de AES (16)
    tiv = AES.block_size
    print(AES.block_size)
    iv = Random.new().read(tiv)

    cifrador = AES.new(clave, modo_aes, iv)

    with open(fichero, 'rb') as entrada:
        with open(ficheroSalida, 'wb') as salida:

            # Escribe el vector de inicialización
            salida.write(iv)

            # Lee bloques del fichero de entrada del tamaño
            # especificado y los escribe en el fichero de salida
            # Si el bloque está vacío sale del bucle
            # Rellena con los espacios necesarios el último bloque
            while True:
                bloque = entrada.read(bs)
                if len(bloque) == 0:
                    break
                else:
                    # Longitud de la cadena para completar el bloque
                    completar = bs - len(bloque) % bs
                    bloque += ' '.encode(encoding='UTF-8') * completar

                # Escribe el bloque cifrado en la salida
                salida.write(cifrador.encrypt(bloque))


def descifrar(clave, fichero):
    '''Descifra un fichero cifrado con AES.
       @param clave: la clave de cifrado
       @param fichero: la localización del fichero a descifrar
    '''
    clave = get_clave(clave)
    bs = 1024
    ficheroSalida = fichero
    modo_aes = AES.MODE_CBC

    with open(fichero, 'rb') as entrada:
        with open(ficheroSalida, 'wb') as salida:

            iv = entrada.read(AES.block_size)
            descifrador = AES.new(clave, modo_aes, iv)

            while True:
                bloque = entrada.read(bs)
                if len(bloque) == 0:
                    break
                salida.write(descifrador.decrypt(bloque))

def get_clave(password):
    ''' Genera un resumen sha-256 a partir de una cadena de texto
        @param password: la cadena de texto
        return: el resumen
    '''
    return SHA256.new(password).digest()