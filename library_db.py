import sqlite3
import pandas as pd

def searchforAuthorAndTitles(name):
    # Creating cursor object using connection object
    cursor = conn.cursor()
    print(name)
    # executing our sql query
    cursor.execute("""SELECT p.Title  
            FROM (Publication as p join Composes as c on p.ID=c.PublicationID) join Author as a on c.AuthorID=a.ID
            WHERE a.FirstName= ? and a.LastName= ? """,((name[0]),(name[1])))
    result=cursor.fetchall()
    print("Showing Publications of Author {} {}\n   Title".format(name[0],name[1]))
    for i in range(len(result)):
        print("{} ".format(i+1), result[i][0])

    choice=int(input("If you want to show more information about one Publication press the number next to him\nElse press -1 to get back\n"))
    if choice==-1: makechoice()

    publicationInfo(choice)

def publicationInfo(title):
    cursor = conn.cursor()
    print(title)
    # executing our sql query
    cursor.execute("""SELECT p.Title , ar.DOI , ar.[Print ISSN], ar.[Electronic ISSN], ar.[Online ISSN], ar.Conference
            FROM ((Article as ar join Publication as p on p.ID=ar.ID) join Composes as c on c.PublicationID=p.ID) join Author as a on a.ID=c.AuthorID
            WHERE p.Title=?""", (title))
    result=cursor.fetchall()
    print("Title   DOI    Print ISSN    Electronic ISSN     Online ISSN     Conference     Science Magazine\n")
    for i in range(len(result)):
        print("{} ".format(i+1), result[i][0], result[i][1], result[i][2], result[i][3], result[i][4,], result[i][5] )

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
    author=int(input("If you want to show more information about one Author press the number next to him \nElse press -1 to get back\n"))
    if author==-1: makechoice()

    searchforAuthorAndTitles(result[author-1])


def searchforTitle(title):
    cursor = conn.cursor()
    cursor.execute("SELECT p.Title  FROM Publication as p  WHERE p.Title like :title ", (f'%{title}%',))
    result=cursor.fetchall()
    print("Titles")
    for i in range(len(result)):
        print("{} ".format(i+1),result[i][0])
    choice=int(input("If you want to show more information about one Publication press the number next to him\nElse press -1 to get back\n"))
    if choice==-1: makechoice()

    publicationInfo(choice)
    
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

def makechoice():
    print("What do you want to search for?")

    
    while (True):
        choice=input("Press 1 for Author \nPress 2 for Title \nPress 3 for general search of subject/keyword \nPress -1 to exit\n")
        match choice:
            case "1":
                name=input("Type the author you are looking for\n")
                searchforAuthor(name)
            case "2":
                title=input("Type the Title you are looking for\n")
                searchforTitle(title)
            case "3":
                keyword=input("Type the keyword you are looking for\n")
                searchforKeyword(keyword)
            case "-1":break

conn=sqlite3.connect('Scientific_Libary.db')

print("Connected to SQLite")
 
makechoice()

conn.close()