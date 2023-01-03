import upload_file
import library_db
import log_in
import sqlite3

if __name__=="__main__":

    while(True):
        conn=sqlite3.connect('Scientific_Libary.db')
        option=input("If you want to sign in press 'Sign in'\nIf you don't have an account and want to sign up press 'Sign up'\nElse press quit to exit program\n")
        if (option=="Sign up"):
            log_in.sign_up(conn)
        elif (option=="Sign in"):
            while (True):
                logStatus=log_in.sign_in(conn)

                if logStatus:
                    print("Login successfull.")
                    fun=input("Do you want to read articles and books or upload files?(Read/Upload/ Back to go back)\n")

                    print("Connected to SQLite")
                    while(True):
                        if fun=="Read" or fun=="read":
                            library_db.makechoice(conn)
                            break
                        elif fun=="Upload" or fun=="upload":
                            upload_file.uploadchoice(conn)
                            break
                        elif fun=="Back" or fun=="back":
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
        