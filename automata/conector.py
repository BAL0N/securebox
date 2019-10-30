import mysql.connector
import constants

c = mysql.connector.connect(**constants.CREDENTIALS)

def getData(name, hash):
    cursor = c.cursor(buffered=True)
    cursor.execute('select * from bin where 1=1 and name=%s and name=%s', (name, name))
    data = cursor.fetchall()
    return data
    cursor.close()
    
c.close

