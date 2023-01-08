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

def sign_up(conn):
    while(True):
        username=input("Type the username you want:")
        if username=="back" or username=="Back": break
        cursor = conn.cursor()
        cursor.execute("""SELECT u.UserID
                FROM  User as u
                WHERE u.UserID=?""",(username,))
        result=cursor.fetchall()

        if len(result)>0:
            print("Username already exists try another one. Or type 'back' to go back")
        else:
            while(True):
                password=input("Type the password you want to use:")

                user_sql='''INSERT INTO User(UserID, Password)
                    VALUES(?,?)'''

                cursor.execute(user_sql,(username, password))
                conn.commit()
                break
            print("Sign up successfull.")
            break