import json
import boto3
from flask import Flask, render_template, url_for, request, redirect
import pymysql
from botocore.exceptions import ClientError
from websocket import create_connection

application = Flask(__name__)

@application.route('/')
def homePage():
    return render_template("home.html")

@application.route('/about', methods=['GET'])
def aboutPage():
    return render_template("about.html")
    
@application.route('/cakes', methods=['GET'])
def cakesPage():
    return render_template("cakes.html")

@application.route('/contact', methods=['GET'])
def contactPage():
    return render_template("contact.html")


@application.route('/orderNow')
def home():
    return render_template("orderNow.html")

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

@application.route('/upload', methods=['GET','POST'])
def upload():
    file = request.files['myfile'].filename
    s3 = boto3.resource('s3')

    s3.Bucket('cake-design-recommendation-client').put_object(Key=file, Body=request.files['myfile'])

    return '<h1>File saved to S3</h1>'

@application.route('/chat', methods=['GET'])
def chat():
    return render_template('/chat.html')

@application.route('/connect_to_admin',methods=['POST', 'GET'])
def chat_with_store():
    output = request.form.to_dict()
    user_name = output["user_name"]
    print(user_name)
    ws = create_connection("wss://1ltd3i86cl.execute-api.us-east-1.amazonaws.com/production?userid=bob")
    json_data = '{"Msg":"hello","ReceiverID":"admin","action":"sendmsg"}'
    json_object = json.loads(json_data)
    ws.send(json.dumps(json_object))

    message = ws.recv()
    print(message)
    html_content = f"<!DOCTYPE html><html><body><script>\
        window.alert('{message}')</script></body></html>"
    with open("templates/warning_message.html", "w") as html_file:
        html_file.write(html_content)
    return render_template("/warning_message.html")
    

@application.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    phoneNumber = output["phoneNumber"]
    password = output["password"]
    cake = output["cakes"]
    
    db = connectToRDS()
    cursor = db.cursor()

    if checkUserExist(cursor, phoneNumber) == True and checkUserPassword(cursor, phoneNumber, password) == True:
        insertNewOrder(db, cursor, phoneNumber, cake)
        return render_template('success.html')
    else:
        return render_template('fail.html')


if __name__ == "__main__":
    application.run(debug=True)