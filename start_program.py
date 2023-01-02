import upload_file
import library_db
import sqlite3

if __name__=="__main__":

    fun=input("Do you want to read articles and books or upload files?(Read/Upload)\n")

    conn=sqlite3.connect('Scientific_Libary.db')

    print("Connected to SQLite")

    if fun=="Read" or fun=="read":
        library_db.makechoice(conn)
    elif fun=="Upload" or fun=="upload":
            upload_file.uploadchoice(conn)

    conn.close()