import sqlite3

def sign_in(conn):
    username=input("Type your username:") 
    password=input("Type your password:") 
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT u.UserID, u.Password
            FROM  User as u
            WHERE u.UserID=?""",(username,))
    result=cursor.fetchall()

    if(result[0][0]==username) and (result[0][1]==password):
        return True
    else:
        return False
