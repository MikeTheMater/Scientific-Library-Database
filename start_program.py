import upload_file
import library_db
import log_in
import sqlite3

if __name__=="__main__":
    conn=sqlite3.connect('Scientific_Libary.db')

    while (True):
        logStatus=log_in.sign_in(conn)

        if logStatus:
            print("Login successfull.")
            fun=input("Do you want to read articles and books or upload files?(Read/Upload)\n")

            

            print("Connected to SQLite")
            while(True):
                if fun=="Read" or fun=="read":
                    library_db.makechoice(conn)
                    break
                elif fun=="Upload" or fun=="upload":
                    upload_file.uploadchoice(conn)
                    break
                else:
                    input("Wrong input, try again.\n")

            conn.close()
            break
        else:
            print("Login failed. Try again.")
        