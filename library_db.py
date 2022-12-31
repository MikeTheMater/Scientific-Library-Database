import sqlite3
import string as str

#search for the publication titles that an author has writen
def searchforAuthorAndTitles(name):
    # Creating cursor object using connection object
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT p.Title  
            FROM (Publication as p join Composes as c on p.ID=c.PublicationID) join Author as a on c.AuthorID=a.ID
            WHERE a.FirstName= ? and a.LastName= ? """,((name[0]),(name[1])))
    result=cursor.fetchall()
    print("Showing Publications of Author {} {}\n   Title".format(name[0],name[1]))
    for i in range(len(result)):
        print("{} ".format(i+1), result[i][0])
 
    choice=int(input("If you want to show more information about one Publication press the number next to its title \nElse press -1 to get back\n"))
    if choice!=-1: publicationInfo(result[choice-1][0])
    

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
    
    while(True):
        choice=int(input("Press 1 to show the Authors \nPress 2 to show References \nPress 3 to show citations \nPress 4 to show Abstract \nPress -1 to exit\n"))
        
        match choice:
            case 1:
                showAuthors(title)
                back=input("Do you want to return to Publication's information?(Yes/No)(Default Yes)\n")
                if(back=="No"):
                    ex=input("Do you want to search for something else?(Yes/No)\n")
                    if (ex=="Yes"): 
                        return   
                    else: 
                        quit()
                elif (back=="Yes"):
                    publicationInfo(title)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case 2:
                showReferences(title)
                back=input("Do you want to return to Publication's information?(Yes/No)(Default Yes)\n")
                if(back=="No"):
                    ex=input("Do you want to search for something else?(Yes/No)\n")
                    if (ex=="Yes"): 
                        return
                    else: 
                        quit()
                elif (back=="Yes"):
                    publicationInfo(title)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case 3:
                back=input("Do you want to return to Publication's information?(Yes/No)(Default Yes)\n")
                if(back=="No"):
                    ex=input("Do you want to search for something else?(Yes/No)\n")
                    if (ex=="Yes"): 
                        return
                    else: 
                        quit()
                elif (back=="Yes"):
                    publicationInfo(title)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case 4:
                back=input("Do you want to return to Publication's information?(Yes/No)(Default Yes)\n")
                if(back=="No"):
                    ex=input("Do you want to search for something else?(Yes/No)\n")
                    if (ex=="Yes"): 
                        return
                    else: 
                        quit()
                elif (back=="Yes"):
                    publicationInfo(title)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case -1:
                return
    

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

    print("Do you want to go to an Author's profile?")

    while(True):
        author=input("Press the number next to the author you want or Press -1 to go back.\n")
        if author.isnumeric()==False:print("Wrong insertion type again.\n")
        elif int(author)>0 and int(author)<len(result): 
            AuthorProfile(result[int(author)-1][0],result[int(author)-1][1])
            break
        elif author=="-1":
            break
        else:print("Wrong insertion type again.\n")


def AuthorProfile(fname,lname):
    cursor = conn.cursor()
    # executing our sql query
    print(fname,lname)
    #find publications each year
    
    cursor.execute("""SELECT p.Year, count(*) as "Number of Publications"
                    FROM (Author as a JOIN Composes as c on a.ID= c.AuthorID) JOIN Publication as p on c.PublicationID= p.ID
                    WHERE a.FirstName=? and a.LastName= ?
                    GROUP by a.LastName, p.Year
                    ORDER by p.Year""", (fname,lname,))
    result=cursor.fetchall()
    
    print(" Number of publications for {} {} each year.".format(fname,lname))
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1])
    
    cursor.execute("""SELECT  a.FirstName ,a.LastName, count(*) as "Number of Collaborations"
                    FROM Author as a JOIN Composes as c on a.ID= c.AuthorID
                    WHERE c.PublicationID in ( SELECT DISTINCT c.PublicationID
                                                FROM Author as a JOIN Composes as c on a.ID= c.AuthorID
                                                WHERE a.FirstName= ? AND a.LastName= ?)
                                             AND a.FirstName!= ? AND a.LastName!= ?
                    GROUP by a.LastName, a.FirstName
                    ORDER by "Number of Collaborations" DESC, a.LastName
                    LIMIT 2""", (fname,lname,fname,lname,))
    result=cursor.fetchall()
    if(len(result)>0):
        print(" Top 2 co-authors of {} {} and the number of their common publications.".format(fname,lname))
        for i in range(len(result)):
            print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1], " ", result[i][2])
        
        while(True):
            co_author=int(input("If you want to view a co author's profile press the number next to him.\nElse press -1\n"))
            match co_author:
                case 1:
                    AuthorProfile(result[0][0], result[0][1])
                    break
                case 2:
                    AuthorProfile(result[1][0], result[1][1])
                    break
                case -1:
                    break
                case other:
                    print("No match, type again.\n")

    
    publ=input("Do you want to show the author's ({} {}) articles and books?(Yes to show/No to go back)\n".format(fname,lname))

    match publ:
        case "Yes":
            searchforAuthorAndTitles([fname,lname])
        case "No":
            return

#search for Author's First and Last name based on the Name that user typed
def searchforAuthor(name):
    name=name.split(" ")
    if len(name)==1:
        # Creating cursor object using connection object
        cursor = conn.cursor()
        
        # executing our sql query
        cursor.execute("SELECT a.FirstName, a.LastName  FROM Author as a  WHERE a.LastName= :name or a.FirstName= :name ", {'name':name[0]})
        result=cursor.fetchall()
        if(len(result)>0):
            print("Authors\n First Name  Last Name")
            for i in range(len(result)):
                
                print("{} ".format(i+1),result[i][0], " ",result[i][1])
            author=int(input("If you want to show more information about one Author press the number next to him to go to his profile \nElse press -1 to get back\n"))
            if author==-1: makechoice()
            else:  AuthorProfile(result[author-1][0],result[author-1][1])
        else: print("No match")
    elif len(name)==2:
        # Creating cursor object using connection object
        cursor = conn.cursor()
        
        # executing our sql query
        cursor.execute("SELECT a.FirstName, a.LastName  FROM Author as a  WHERE (a.LastName= :name2 and a.FirstName= :name1) or (a.LastName= :name1 and a.FirstName= :name2) ", {'name1':name[0],'name2':name[1]})
        result=cursor.fetchall()
        if(len(result)>0):
            print("Authors\n First Name  Last Name")
            for i in range(len(result)):
                print("{} ".format(i+1),result[i][0], " ",result[i][1])
            author=int(input("If you want to show more information about one Author press the number next to him to go to his profile \nElse press -1 to get back\n"))
            if author==-1: makechoice()
            else:AuthorProfile(result[author-1][0],result[author-1][1])
        else: print("No match")
    

#search for titles that have the words that the user gives
def searchforTitle(title):
    cursor = conn.cursor()
    cursor.execute("SELECT p.Title  FROM Publication as p  WHERE p.Title like :title ", (f'%{title}%',))
    result=cursor.fetchall()
    if(len(result)>0):
        print("Titles")
        for i in range(len(result)):
            print("{} ".format(i+1),result[i][0])
        choice=int(input("If you want to show more information about one Publication press the number next to him\nElse press -1 to get back\n"))
        if choice==-1: makechoice()

        else:publicationInfo(result[choice-1][0])
    else:print("No match")

#search for titles that are about the given keyword
def searchforKeyword(keyword):
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT a_k1.Keywords, p1.Title, 'Article'
    FROM Publication as p1 JOIN Article_Keywords as a_k1 on p1.ID= a_k1.ID,
            Publication as p2 JOIN Article_Keywords as a_k2 on p2.ID= a_k2.ID
    WHERE a_k1.Keywords like ?
    UNION
    SELECT DISTINCT c_k1.Keywords, c1.Title, 'Chapter'
    FROM Chapter as c1 JOIN Chapter_Keywords as c_k1 on c1.ID= c_k1.ID,
            Chapter as c2 JOIN Chapter_Keywords as c_k2 on c2.ID= c_k2.ID
    WHERE c_k1.Keywords like ?
    ORDER by a_k1.Keywords, c_k1.Keywords """, (f'%{keyword}%',f'%{keyword}%',))
    result=cursor.fetchall()
    print("Keyword  Title")
    for i in range(len(result)):
        
        print("{} ".format(i+1),result[i][0], " ",result[i][1], " ", result[i][2])

def makechoice():
    while (True):
        print("What do you want to search for?")
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
            case "-1":quit()
            case other:
                print("Wrong input type again.")

#def back():


conn=sqlite3.connect('Scientific_Libary.db')

print("Connected to SQLite")
 
makechoice()

conn.close()