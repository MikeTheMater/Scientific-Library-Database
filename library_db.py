import sqlite3
import pandas as pd

#search for the publication titles that an author has writen
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
 
    choice=int(input("If you want to show more information about one Publication press the number next to its title \nElse press -1 to get back\n"))
    if choice==-1: makechoice()

    publicationInfo(result[choice-1][0])

#search for information on the publication with the given title
def publicationInfo(title):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT Distinct p.Title , ar.DOI , ar.[Print ISSN], ar.[Electronic ISSN], ar.[Online ISSN], ar.Conference, ar.[Science Magazine]
            FROM ((Article as ar join Publication as p on p.ID=ar.ID) join Composes as c on c.PublicationID=p.ID) join Author as a on a.ID=c.AuthorID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("Title   DOI    Print ISSN    Electronic ISSN     Online ISSN     Conference     Science Magazine")
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1],"  ", result[i][2],"  " ,result[i][3],"  ", result[i][4],"  ", result[i][5], " ", result[i][6] )
    
    choice=int(input("Press 1 to show the Authors \nPress 2 to show References \nPress 3 to show citations \nPress 4 to show Abstract \nPress -1 to exit\n"))
    
    match choice:
        case 1:
            showAuthors(title)
        case 2:
            showReferences(title)
        case 3:
            showCitations(title)
        case 4:
            showAbstract(title)
        case -1:makechoice()

def showAbstract(title):
    cursor = conn.cursor()
    # executing our sql query
    print(title)
    cursor.execute("""SELECT p.Abstract
            FROM Publication as p
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("Abstract")
    for i in range(len(result)):
        print(result[i][0])


def showCitations(title):
    cursor = conn.cursor()
    # executing our sql query
    print(title)
    cursor.execute("""SELECT a_c.Citations
            FROM (Article_Citations as a_c join Article as c on a_c.ID=c.ID) join Publication as p on c.ID=p.ID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("Citations")
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0])

def showReferences(title):
    cursor = conn.cursor()
    # executing our sql query
    print(title)
    cursor.execute("""SELECT a_r.[References]
            FROM (Article_References as a_r join Article as c on a_r.ID=c.ID) join Publication as p on c.ID=p.ID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("References")
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0])

#search for the authors of the publication and their affiliation
def showAuthors(title):
    cursor = conn.cursor()
    # executing our sql query
    print(title)
    cursor.execute("""SELECT a.FirstName, a.LastName, c.Affiliation
            FROM (Author as a join Composes as c on a.ID=c.AuthorID) join Publication as p on c.PublicationID=p.ID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("   First Name     Last Name      Affiliation")
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1],"  ", result[i][2])

#search for Author's First and Last name based on the Name that user typed
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

#search for titles that have the words that the user gives
def searchforTitle(title):
    cursor = conn.cursor()
    cursor.execute("SELECT p.Title  FROM Publication as p  WHERE p.Title like :title ", (f'%{title}%',))
    result=cursor.fetchall()
    print("Titles")
    for i in range(len(result)):
        print("{} ".format(i+1),result[i][0])
    choice=int(input("If you want to show more information about one Publication press the number next to him\nElse press -1 to get back\n"))
    if choice==-1: makechoice()

    publicationInfo(result[choice-1][0])

#search for titles that are about the given keyword
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