from random import choice


def generatorClave(num, let, spe, long):

    valores = ''
    valoresNumericos = '0123456789'
    valoresLetras = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    valoresEspeciales = '<=>@#%&+'
    valoresCompletos = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

    if num == 1:
        valores = valores + valoresNumericos
    if let == 1:
        valores = valores + valoresLetras
    if spe == 1:
        valores = valores + valoresEspeciales
    if num == 0 and let == 0 and let == 0:
        valores = valores + valoresCompletos

    passwd = ''
    passwd = passwd.join([choice(valores) for i in range(int(long))])
    return passwd

