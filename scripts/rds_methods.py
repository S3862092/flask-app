import pymysql

def connectToRDS():
    #connect to database
    db = pymysql.connect(host = 'database-1.cqnbq7qymqyf.us-east-1.rds.amazonaws.com', 
                        user = 'admin', 
                        password = 'admin123')
    return db

def insertNewUser(db, cursor, username, password, phoneNumber):
    cursor.execute('use store')
    sql = '''
    INSERT INTO users
    VALUES (%s, %s, %s);
    '''
    cursor.execute(sql, (phoneNumber, username, password))
    db.commit() #A COMMIT means that the changes made in the current transaction are made permanent and become visible to other sessions

def insertNewOrder(db, cursor, phoneNumber, cake):
    # Add a userId in the user table and set it to Auto increment
    sql = '''
    INSERT INTO orders
    VALUES (NULL, %s, curdate(), %s);'''
    cursor.execute(sql, (cake, phoneNumber))
    db.commit()

def checkUserExist(cursor, phoneNumber):
    cursor.execute('use store')
    sql = '''
    SELECT * 
    FROM users
    WHERE phoneNumber = ''' + phoneNumber
    cur = cursor.execute(sql)
    if cur == 1:
        return True
    else:
        return False
    
def checkUserPassword(cursor, phoneNumber, password):
    cursor.execute('use store')
    sql = '''
    SELECT password 
    FROM users
    WHERE phoneNumber = %s''' 
    cursor.execute(sql, (phoneNumber))
    row = cursor.fetchone()
    actualPassword = ""
    while row is not None:
        actualPassword = row
        row = cursor.fetchone()

    actualPasswordStr = actualPassword[0]

    if password == actualPasswordStr:
        return True
    else:
        return False