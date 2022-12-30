import sqlite3

try:
    conn=sqlite3.connect('Scientific_Library.db')

    print("Connected to SQLite")
 
    # Getting all tables from sqlite_master
    sql_query = """SELECT DISTINCT a.FirstName, a.LastName
    FROM Author as a, Author as b
    WHERE a.LastName=b.LastName AND a.FirstName!=b.FirstName"""
 
    # Creating cursor object using connection object
    cursor = conn.cursor()
     
    # executing our sql query
    cursor.execute(sql_query)
    print("List of tables\n")
     
    # printing all tables list
    print(cursor.fetchall())
 
except sqlite3.Error as error:
    print("Failed to execute the above query", error)

finally:
   
    # Inside Finally Block, If connection is
    # open, we need to close it
    if conn:
         
        # using close() method, we will close
        # the connection
        conn.close()
         
        # After closing connection object, we
        # will print "the sqlite connection is
        # closed"
        print("the sqlite connection is closed")

