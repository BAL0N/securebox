import mysql.connector

from code.Crypto import getHash
from code.Objects import Sesion

cred = {
    'user': 'root',
    'password': 'b6qeyuge',
    'host': 'localhost',
    'database': 'securebox'
}
c = mysql.connector.connect(**cred)


def getSesion(name, password):
    hashedpass = getHash(password)

    cursor = c.cursor(buffered=True)
    cursor.execute('select id, name, hash, now() from users where name=%s and hash=%s', (name, hashedpass))
    data = cursor.fetchone()

    try:
        if hashedpass == data[2]:
            sesion = Sesion(data[0], data[1], data[2], data[3])
            return sesion
    except TypeError:
        sesion = False
        return sesion

    cursor.close()


def setSesion(name, password):
    hashedpass = getHash(password)

    cursor = c.cursor()
    cursor.execute('insert into users(name, hash) values(%s, %s)', (name, hashedpass))
    data = cursor.fetchone()

    cursor.close()


def setData(name, algorithm, property, hash, cryptedfile, cryptedpassword, cryptedinfo, site, username, mail, notes):
    args = (name, algorithm, property, hash, cryptedfile, cryptedpassword, cryptedinfo, site, username, mail, notes)

    cursor = c.cursor()
    cursor.execute('insert into secrets(name, algorithm, property, hash, cryptedfile, cryptedpassword, cryptedinfo, site, username, mail, notes) '
                   'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', args)
    c.commit()
    cursor.close()


def getData(property):
    cursor = c.cursor()
    cursor.execute('select id,name,version,algorithm,site,username,mail,notes from secrets where property=%s and property=%s',
                   (property, property))

    data = cursor.fetchall()

    return data
    cursor.close()


def getDataById(property, id):
    cursor = c.cursor()
    cursor.execute('select id,name,version,algorithm,site,username,mail,notes from secrets where property=%s and id=%s',
                   (property, id))

    data = cursor.fetchone()

    return data
    cursor.close()


def updateData(name, version, algorithm, password, site, username, mail, file, cryptpass, notes, property, id):
    cursor = c.cursor()
    args = (name, version, algorithm, password, site, username, mail, file, cryptpass, notes, property, id)
    cursor.execute('update secrets set name=%s,version=%s,algorithm=%s,hash=%s,site=%s,username=%s,mail=%s,crypt=%s,cryptpass=%s,notes=%s where property=%s and id=%s ', args)
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


c.close

