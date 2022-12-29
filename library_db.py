import sqlite3
import pandas as pd

def searchforAuthorAndTitles(name):
    name=name.split(" ")
    if len(name)==1:
        # Creating cursor object using connection object
        cursor = conn.cursor()
        
        # executing our sql query
        cursor.execute("SELECT a.FirstName, a.LastName, p.Title  FROM (Publication as p join Composes as c on p.ID=c.PublicationID), Author as a  WHERE c.AuthorID=a.ID and a.LastName= :name or a.FirstName= :name ", {'name':name[0]})
        print(cursor.fetchall())
    elif len(name)==2:
        # Creating cursor object using connection object
        cursor = conn.cursor()
        
        # executing our sql query
        cursor.execute("SELECT a.FirstName, a.LastName, p.Title  FROM (Publication as p join Composes as c on p.ID=c.PublicationID), Author as a  WHERE c.AuthorID=a.ID and (a.LastName= :name2 and a.FirstName= :name1) ", {'name1':name[0],'name2':name[1]})
        print(cursor.fetchall())

def searchforAuthor(name):
    name=name.split(" ")
    if len(name)==1:
        # Creating cursor object using connection object
        cursor = conn.cursor()
        
        # executing our sql query
        cursor.execute("SELECT a.FirstName, a.LastName  FROM Author as a  WHERE a.LastName= :name or a.FirstName= :name ", {'name':name[0]})
        result=cursor.fetchall()
        print("Authors\n First Name  Last Name")
        for i in range(len(result)):
            
            print("{} ".format(i+1),result[i][0], " ",result[i][1])
    elif len(name)==2:
        # Creating cursor object using connection object
        cursor = conn.cursor()
        
        # executing our sql query
        cursor.execute("SELECT a.FirstName, a.LastName  FROM Author as a  WHERE (a.LastName= :name2 and a.FirstName= :name1) or (a.LastName= :name1 and a.FirstName= :name2) ", {'name1':name[0],'name2':name[1]})
        result=cursor.fetchall()
        print("Authors\n First Name  Last Name")
        for i in range(len(result)):
            print("{} ".format(i+1),result[i][0], " ",result[i][1])

def searchforTitle(title):
    cursor = conn.cursor()
    cursor.execute("SELECT p.Title  FROM Publication as p  WHERE p.Title like :title ", (f'%{title}%',))
    result=cursor.fetchall()
    print("Titles")
    for i in range(len(result)):
        print("{} ".format(i+1),result[i][0])
    
def searchforKeyword(keyword):
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT a_k1.Keywords, p1.Title
    FROM Publication as p1 JOIN Article_Keywords as a_k1 on p1.ID= a_k1.ID,
            Publication as p2 JOIN Article_Keywords as a_k2 on p2.ID= a_k2.ID
    WHERE a_k1.Keywords like ?
    UNION
    SELECT DISTINCT c_k1.Keywords, c1.Title
    FROM Chapter as c1 JOIN Chapter_Keywords as c_k1 on c1.ID= c_k1.ID,
            Chapter as c2 JOIN Chapter_Keywords as c_k2 on c2.ID= c_k2.ID
    WHERE c_k1.Keywords like ?
    ORDER by a_k1.Keywords, c_k1.Keywords """, (f'%{keyword}%',f'%{keyword}%',))
    result=cursor.fetchall()
    print("Keyword  Title")
    for i in range(len(result)):
        
        print("{} ".format(i+1),result[i][0], " ",result[i][1])

conn=sqlite3.connect('Scientific_Libary.db')

print("Connected to SQLite")
 
print("What do you want to search for?")

choice=input("Press 1 for author \nPress 2 for Title \nPress 3 for general search of subject/keyword\n")

match choice:
    case "1":
        input=input("Type the author you are looking for\n")
        searchforAuthor(input)
    case "2":
        input=input("Type the Title you are looking for\n")
        searchforTitle(input)
    case "3":
        input=input("Type the keyword you are looking for\n")
        searchforKeyword(input)

conn.close()