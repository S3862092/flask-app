'''
ONLY RUN THIS SCRIPT ONCE TO INSTANTIATE NEW TABLES in database-1 
'''

import pymysql

#connect to database
db = pymysql.connect(host = 'database-1.cqnbq7qymqyf.us-east-1.rds.amazonaws.com', 
                     user = 'admin', 
                     password = 'admin123')

cursor = db.cursor()

#CREATE DATABASE STORE
sql = '''create database store'''
cursor.execute(sql)

sql = '''use store'''
cursor.execute(sql)

#CREATE TABLE USERS
sql = '''
create table users(
    phoneNumber int PRIMARY KEY,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);
'''

cursor.execute(sql)

#CREATE TABLE ORDERS
sql = '''
create table orders(
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cake varchar(255) NOT NULL,
    dt DATE NOT NULL,
    phoneNumber int,
	FOREIGN KEY (phoneNumber) REFERENCES users(phoneNumber)
);
'''
cursor.execute(sql)