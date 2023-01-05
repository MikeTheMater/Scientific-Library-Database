import upload_file
import library_db
import log_in
import sqlite3

if __name__=="__main__":

    while(True):
        conn=sqlite3.connect('Scientific_Libary.db')
        option=input("If you want to sign in type 'Sign in'\nIf you don't have an account and want to sign up type 'Sign up'\nElse type quit to exit program\n")
        if (option=="Sign up"):
            log_in.sign_up(conn)
        elif (option=="Sign in"):
            while (True):
                logStatus=log_in.sign_in(conn)

                if logStatus:
                    print("Login successfull.")
                    

                    print("Connected to SQLite")
                    while(True):
                        fun=input("Do you want to read articles and books or upload files?(Read/Upload/ Back to go back)\n")
                        if fun.lower()=="read":
                            library_db.makechoice(conn)
                            break
                        elif fun.lower()=="upload":
                            upload_file.uploadchoice(conn)
                            break
                        elif fun.lower()=="back":
                            break
                        else:
                            input("Wrong input, try again.\n")

                    conn.close()
                    break
                else:
                    print("Login failed. Try again.")
        elif(option=="quit"):
            quit()
        else:
            print("Wrong input, try again.")
        