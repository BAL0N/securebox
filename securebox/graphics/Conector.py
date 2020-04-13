import mysql.connector

from Cryptos import getHash
from Objects import Sesion
from credentials import cred

c = mysql.connector.connect(**cred)


def getSesion(name, hash):
    cursor = c.cursor(buffered=True)
    cursor.execute('select id, name, hash, now() from users where name=%s and hash=%s', (name, hash))
    data = cursor.fetchone()

    try:
        if hash == data[2]:
            sesion = Sesion(data[0], data[1], data[2], data[3])
            return sesion
    except TypeError:
        sesion = False
        return sesion

    cursor.close()


def setSesion(name, hash):
    cursor = c.cursor()
    cursor.execute('insert into users(name, hash) values(%s, %s)', (name, hash))
    data = cursor.fetchone()
    cursor.close()


def setData(name, algorithm, property, hash, cryptedfile, cryptedpassword, cryptedinfo, site, username, mail, notes):
    args = (name, algorithm, property, hash, cryptedfile, cryptedpassword, cryptedinfo, site, username, mail, notes)
    cursor = c.cursor()
    cursor.execute('insert into secrets(name, algorithm, property, hash, cryptedfile, cryptedpassword, cryptedinfo, site, username, mail, notes) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', args)
    c.commit()
    cursor.close()


def getData(property):
    cursor = c.cursor()
    cursor.execute('select id,name,version,algorithm,site,username,mail,notes from secrets where property=%s and property=%s', (property, property))

    data = cursor.fetchall()
    return data

    cursor.close()


def getDataById(property, id):
    cursor = c.cursor()
    cursor.execute('select id,name,version,algorithm,cryptedpassword,cryptedinfo,cryptedfile,site,username,mail,notes from secrets where property=%s and id=%s', (property, id))

    data = cursor.fetchone()
    return data

    cursor.close()


def updateData(name, version, algorithm, password, cryptedpassword, cryptedinfo, cryptedfile, site, username, mail, notes, property, id):
    cursor = c.cursor()
    args = (name, version, algorithm, password, cryptedpassword, cryptedinfo, cryptedfile, site, username, mail, notes, property, id)
    cursor.execute('update secrets set name=%s,version=%s,algorithm=%s,hash=%s,cryptedpassword=%s,cryptedinfo=%s,cryptedfile=%s,site=%s,username=%s,mail=%s,notes=%s where property=%s and id=%s ', args)
    cursor.close()


def deleteData(id, name):
    sql = "delete from secrets where id=%s and name=%s"
    args = (id, name)

    cursor = c.cursor()
    cursor.execute(sql, args)
    c.commit()
    cursor.close()


def cryptBool(id):
    cursor = c.cursor()
    args = (id, id)
    cursor.execute('select count(cryptedfile) from secrets where id=%s and id=%s', args)
    data = cursor.fetchone()[0]
    return data

    cursor.close()


def getCryptedFile(id, name):
    sql = "select cryptedfile from secrets where id=%s and name=%s"
    args = (id, name)

    cursor = c.cursor()
    cursor.execute(sql, args)

    data = cursor.fetchone()[0]
    return data

    cursor.close()


def getCryptedPassword(id, name):
    sql = "select cryptedpassword from secrets where id=%s and name=%s"
    args = (id, name)

    cursor = c.cursor()
    cursor.execute(sql, args)

    data = cursor.fetchone()[0]
    return data

    cursor.close()


def getCryptedInfo(id, name):
    sql = "select cryptedinfo from secrets where id=%s and name=%s"
    args = (id, name)

    cursor = c.cursor()
    cursor.execute(sql, args)

    data = cursor.fetchone()[0]
    return data

    cursor.close()


def getHashData(id, name):
    cursor = c.cursor()
    cursor.execute('select hash from secrets where name=%s and id=%s', (name, id))
    data = cursor.fetchone()
    return data[0]
    cursor.close()


def existUser(name):
    cursor = c.cursor()
    cursor.execute('select count(*) from users where name=%s and name=%s', (name, name))
    data = cursor.fetchone()
    if data[0] == 1:
        return True
    else:
        return False
    cursor.close()

c.close

