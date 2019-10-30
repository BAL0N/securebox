import os
import hashlib
from hashlib import sha256
from os import sys
import conector
import constants
from builtins import input

validall = False
Answer = constants.SYMBOL_NO

# Obtención de suma de verificación de secuencia binaria
def SHA256_Checksum(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# Método principal de lógica de validación
def logicValidation(args):
    try:
        pathX = os.path.realpath(args)
        hashX = SHA256_Checksum(pathX)
        
        data = conector.getData(pathX, hashX)
        if not data:
            data = constants.ERROR_NO_DATA + constants.INTRO + constants.QUESTION_NEW_FILE
        else:
            for x in data:
                pathY = x[1]
                hashY = x[2]
                if pathX == pathY and hashX == hashY:
                    data = constants.VALIDATION_OK
                else:
                    data = constants.ERROR_VALDIATION
            
        print(pathX + constants.INTRO + 
              hashX + constants.INTRO +
              str(data) )
        
        if data.strip()[len(data.strip())-1:len(data.strip())] == constants.SHELL and validall is False:
            sn = input('')
            if sn == constants.SYMBOL_SI:
                print('SIIII')
            elif sn == constants.SYMBOL_SI_ALL:
                print('SIIIIIIIIIIIIIIIIII')
            elif sn == constants.SYMBOL_NO_ALL:
                print('NOUUUUUUUU')
            else:
                print('NO')
        
        print(constants.INTRO)
        
    except PermissionError:
        print(constants.ERROR_PERMISSONS + args)

# Método de control de argumentos
def controlArgs(args):
    if os.path.isdir(args):
        for base, dirs, files in os.walk(args):
            for f in files:
                logicValidation(base + constants.SEPARATOR + f)
    elif os.path.isfile(args):
        logicValidation(args)
    else:
        print(constants.ERROR_VALIDACION)

####################################################################################

arguments = sys.argv[1:]

if len(arguments) == 0:
    args = constants.HERE
    controlArgs(args)
else:
    for i in range(0, len(arguments)):
        args = arguments[i]
        controlArgs(args)