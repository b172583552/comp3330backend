import sqlite3

# Connects to database
# The .db file is created automatically if it does not exist
con = sqlite3.connect('caretaker.db')

# Creates table
con.execute("""
CREATE TABLE IF NOT EXISTS USERS (
 ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
 Username TEXT NOT NULL,
 Password TEXT NOT NULL,);
 
 CREATE TABLE IF NOT EXISTS JOBS (
 ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
 UserID  INTEGER
 Organization TEXT NOT NULL,
 JobTitle TEXT NOT NULL,
 Place TEXT NOT NULL,
 JobDetails TEXT NOT NULL,
 JobTime DATETIME DEFAULT current_timestamp, 
 FOREIGN KEY (UserID) references USERS(ID));
 
 """)
# # insert test data
# testData = ['Anthony', 'Ben', 'John', 'Kenneth', 'Loretta']
# for name in testData:
#     insertQuery = "INSERT INTO STUDENT (NAME) values (?);"
#     con.execute(insertQuery, (name,))
con.commit()
con.close()
