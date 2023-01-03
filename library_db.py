import sqlite3

#search for the publication titles that an author has writen
def searchforAuthorAndTitles(name, conn):
    # Creating cursor object using connection object
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT p.Title, "Article"
            FROM (Publication as p join Composes as c on p.ID=c.PublicationID) join Author as a on c.AuthorID=a.ID, Article as ar
            WHERE a.FirstName= ? and a.LastName= ? and ar.ID=p.ID
            UNION
            SELECT p.Title, "Scientific Book"
            FROM (Publication as p join Composes as c on p.ID=c.PublicationID) join Author as a on c.AuthorID=a.ID, Scientific_Book as sb
            WHERE a.FirstName= ? and a.LastName= ? and sb.ID=p.ID""",(name[0],name[1],name[0],name[1]))
    result=cursor.fetchall()
    print("Showing Publications of Author {} {}\n   Title".format(name[0],name[1]))
    for i in range(len(result)):
        print("{} ".format(i+1), result[i][0],"   ", result[i][1])
    
    while(True):
        choice=input("If you want to show more information about one Publication press the number next to its title \nElse press -1 to get back\n")
        if choice.isdigit():
            if int(choice)<=len(result) and int(choice)>0: 
                if result[choice-1][1]=="Article":
                    articleInfo(result[int(choice)-1][0], conn, name, flag)
                elif result[choice-1][1]=="Scientific Book":
                    bookInfo(result[int(choice)-1][0], conn, name)
                return
            
            else:
                print("Wrong input, try again.\n")
        elif choice=="-1": return
        else:print("Wrong input, try again.\n")
    

#search for information on the publication with the given title
def articleInfo(title, conn, name, flag):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT Distinct p.Title , ar.DOI , ar.[Print ISSN], ar.[Electronic ISSN], ar.[Online ISSN], ar.Conference, ar.[Science Magazine]
            FROM ((Article as ar join Publication as p on p.ID=ar.ID) join Composes as c on c.PublicationID=p.ID) join Author as a on a.ID=c.AuthorID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("    Title   DOI    Print ISSN    Electronic ISSN     Online ISSN     Conference     Science Magazine")
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1],"  ", result[i][2],"  " ,result[i][3],"  ", result[i][4],"  ", result[i][5], " ", result[i][6] )
    
    while(True):
        choice=input("Press 1 to show the Authors \nPress 2 to show References \nPress 3 to show Citations \nPress 4 to show Abstract \nPress -1 to exit\n")
        
        match choice:
            case "1":
                showAuthors(title, conn)
                while(True):
                    back=input("Do you want to return to Article's information?(Yes/No)\n")
                    if(back=="No"):
                        if flag==True:
                            searchforAuthorAndTitles(name, conn)
                        elif flag==False:
                            makechoice(conn) 
                        break
                    elif (back=="Yes"):
                        articleInfo(title, conn, name, flag)
                        break
                    else:
                        print("Wrong in typing.\n")
                break
            case "2":
                showReferences(title, conn)
                while(True):
                    back=input("Do you want to return to Article's information?(Yes/No)\n")
                    if(back=="No"):
                        if flag==True:
                            searchforAuthorAndTitles(name, conn)
                        elif flag==False:
                            makechoice(conn) 
                        break
                    elif (back=="Yes"):
                        articleInfo(title, conn, name, flag)
                        break
                    else:
                        print("Wrong in typing.\n")
                break
            case "3":
                showCitations(title, conn)
                while(True):
                    back=input("Do you want to return to Article's information?(Yes/No)\n")
                    if(back=="No"):
                        if flag==True:
                            searchforAuthorAndTitles(name, conn)
                        elif flag==False:
                            makechoice(conn) 
                        break
                    elif (back=="Yes"):
                        articleInfo(title, conn, name, flag)
                        break
                    else:
                        print("Wrong in typing.\n")
                break
            case "4":
                showAbstract(title, conn)
                while(True):
                    back=input("Do you want to return to Article's information?(Yes/No)\n")
                    if(back=="No"):
                        if flag==True:
                            searchforAuthorAndTitles(name, conn)
                        elif flag==False:
                            makechoice(conn) 
                        break
                    elif (back=="Yes"):
                        articleInfo(title, conn, name, flag)
                        break
                    else:
                        print("Wrong in typing.\n")
                break
            case "-1":
                searchforAuthorAndTitles(name, conn)
                break
            case other:
                print("No match, try again.\n")

def bookInfo(title, conn, name):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT Distinct p.Title , sb.[Book Type], sb.[Persistent Link], sb.[Electronic pdf ISBN], sb.[Electronic epub ISBN], sb.[Online ISBN], sb.[Print ISBN]
            FROM ((Scientific_Book as sb join Publication as p on p.ID=sb.ID) join Composes as c on c.PublicationID=p.ID) join Author as a on a.ID=c.AuthorID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("    Title   Persistent Link    Electronic pdf ISBN     Electronic epub ISBN     Online ISBN     Print ISBN")
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1],"  ", result[i][2],"  " ,result[i][3],"  ", result[i][4],"  ", result[i][5], " ", result[i][6] )
    
    while(True):
        choice=input("Press 1 to show the Authors \nPress 2 to show Abstract \nPress 3 to show Chapters \nPress -1 to exit\n")
        
        match choice:
            case "1":
                showAuthors(title, conn)
                back=input("Do you want to return to Book's information?(Yes/No)\n")
                if(back.lower()=="no"):
                    #searchforAuthorAndTitles(name, conn)
                    break
                elif (back.lower()=="yes"):
                    bookInfo(title, conn, name)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case "2":
                showAbstract(title, conn)
                back=input("Do you want to return to Book's information?(Yes/No)\n")
                if(back.lower()=="no"):
                    #searchforAuthorAndTitles(name, conn)
                    break
                elif (back.lower()=="yes"):
                    bookInfo(title, conn, name)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case "3":
                showChapters(title, conn)
                back=input("Do you want to return to Book's information?(Yes/No)\n")
                if(back.lower()=="no"):
                    #searchforAuthorAndTitles(name, conn)
                    break
                elif (back.lower()=="yes"):
                    bookInfo(title, conn, name)
                    break
                else:
                    print("Wrong in typing.\n")
                    
            case "-1":
                break
                #searchforAuthorAndTitles(name, conn)

def showChapters(title, conn):
    cursor = conn.cursor()
    # executing our sql query
    print(title)
    cursor.execute("""SELECT ch.Title
            FROM (Chapter as ch join Scientific_Book as sb on ch.BookID=sb.ID) join Publication as p on p.ID=sb.ID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("Chapters of {}.".format(title))
    for i in range(len(result)):
        print("{} ".format(i+1),result[i][0])

    while(True):
        chapter=input("If you want to see more about a chapter press the number next to it,\n or press -1 to go back.\n")
        if chapter.isnumeric()==False:print("Wrong insertion type again.\n")
        elif int(chapter)>0 and int(chapter)<len(result): 
            chapterInfo(result[int(chapter)-1][0], conn)
            break
        elif chapter=="-1":
            break

def showAbstract(title, conn):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT p.Abstract
            FROM Publication as p
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("Abstract of {}.\n".format(title))
    for i in range(len(result)):
        print(result[i][0])


def showCitations(title, conn):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT a_c.Citations
            FROM (Article_Citations as a_c join Article as c on a_c.ID=c.ID) join Publication as p on c.ID=p.ID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("Citations of {}.\n".format(title))
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0])

def showReferences(title, conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT a_r.[References]
            FROM (Article_References as a_r join Article as c on a_r.ID=c.ID) join Publication as p on c.ID=p.ID
            WHERE p.Title=?""", (title,))
    result=cursor.fetchall()
    print("References of {}.\n".format(title))
    for i in range(len(result)):
        print("{} ".format(i+1),"  " ,result[i][0])

#search for the authors of the publication and their affiliation
def showAuthors(title, conn):
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

    while(True):
        author=input("If you want to visit an author's profile press the number next to him,\n or press -1 to go back.\n")
        if author.isdigit():
            if int(author)>0 and int(author)<=len(result): 
                AuthorProfile(result[int(author)-1][0],result[int(author)-1][1], conn)
                break
            
            else:print("Wrong insertion type again.\n")
        elif author=="-1":
                break
        else:print("Wrong insertion type again.\n")


def AuthorProfile(fname,lname, conn):
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
    
    cursor.execute("""SELECT a_c.Year, count(*) as "Citations per Year"
                        FROM Article_Citations as a_c JOIN (SELECT p.Title
                                                            FROM (Author as a JOIN Composes as c on a.ID= c.AuthorID) JOIN Publication as p on c.PublicationID= p.ID
                                                            WHERE a.FirstName= ? AND a.LastName= ?) as t
                        WHERE instr(a_c.Citations, t.Title)>0
                        GROUP by a_c.Year""", (fname,lname,))
    result=cursor.fetchall()
    if len(result)<0:
        print(" Number of citaitons for {} {} each year.".format(fname,lname))
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
        print(" Top co-authors of {} {} and the number of their common publications.".format(fname,lname))
        for i in range(len(result)):
            print("{} ".format(i+1),"  " ,result[i][0],"  " ,result[i][1], " ", result[i][2])
        
        while(True):
            co_author=input("If you want to view a co author's profile press the number next to him.\nElse press -1\n")
            match co_author:
                case "1":
                    AuthorProfile(result[0][0], result[0][1], conn)
                    return
                    break
                case "2":
                    AuthorProfile(result[1][0], result[1][1], conn)
                    return
                    break
                case "-1":
                    break
                case other:
                    print("No match, type again.\n")
    else: print("{} {} doesn't have co-authors.".format(fname,lname))

    while (True):
        publ=input("Do you want to show the author's ({} {}) articles and books?(Yes to show/No to go back)\n".format(fname,lname))
        match publ.lower():
            case "yes":
                searchforAuthorAndTitles([fname,lname], conn)
                
                break
            case "no":
                break
            case other:
                print("Wrong input, type again.\n")

#search for Author's First and Last name based on the Name that user typed
def searchforAuthor(name, conn, flag):
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

            while(True):
                author=input("If you want to show more information about one Author press the number next to him to go to his profile \nElse press -1 to get back\n")
                if author.isdigit():
                    if int(author)<=len(result) and int(author)>0: 
                        #go to author's profile  
                        AuthorProfile(result[author-1][0],result[author-1][1], conn)
                    else:
                        print("Wrong input, try again.\n")
                elif author=="-1": return
                else:print("Wrong input, try again.\n")
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
            if author==-1: return
            else:#go to author's profile
                AuthorProfile(result[author-1][0],result[author-1][1], conn)
        else: print("No match")
    

#search for titles that have the words that the user gives
def searchforTitle(title, conn, flag):
    cursor = conn.cursor()
    cursor.execute('''SELECT p.Title, "Article"
                    FROM Publication as p JOIN Article as a on p.ID= a.ID
                    WHERE p.Title like :title
                    UNION
                    SELECT p.Title, "Scientific Book"
                    FROM Publication as p JOIN Scientific_Book as sb on p.ID= sb.ID
                    WHERE p.Title like :title
                    ORDER by p.Title ''', (f'%{title}%',))
    result=cursor.fetchall()
    if(len(result)>0):
        print("Titles")
        for i in range(len(result)):
            print("{} ".format(i+1), result[i][0], result[i][1])

        while (True):
            choice=input("If you want to select one publication press the number next to it.\nElse press -1 to go back.\n")

            if int(choice)>0 and int(choice)<=len(result):
                name=findTitlesAuthor(conn, result[int(choice)-1][0])
                if result[int(choice)-1][1]=="Article":
                    #call article info to show more informations about the article
                    articleInfo(result[int(choice)-1][0], conn, name, flag)
                    break
                elif result[int(choice)-1][1]=="Scientific Book":
                    #call bookInfo to show more informations about the book
                    bookInfo(result[int(choice)-1][0], conn, name)
                    break
            elif choice=="-1":
                return
            else:
                print("Wrong input, type again.")
    else:print("No match.")

def findTitlesAuthor(conn, title):
    cursor = conn.cursor()
    cursor.execute('''SELECT a.FirstName, a.LastName
                    FROM (Author as a join Composes as c on a.ID=c.AuthorID) join Publication as p on c.PublicationID=p.ID
                    WHERE p.Title=?''', (title,))
    result=cursor.fetchall()

    name=[result[0][0],result[0][1]]
    return name

#search for titles that are about the given keyword
def searchforKeyword(keyword, conn, flag):
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

    if len(result)>0:
        print("Keyword      Title")
        for i in range(len(result)):
            print("{} ".format(i+1),result[i][0], " ",result[i][1], " ", result[i][2])

        while (True):
            choice=input("If you want to select one publication press the number next to it.\n Else press -1 to go back.\n")

            if int(choice)>0 and int(choice)<=len(result):
                if result[int(choice)-1][2]=="Article":
                    name=findTitlesAuthor(conn,result[int(choice)-1][1])
                    articleInfo(result[int(choice)-1][1], conn, name)
                    break
                elif result[int(choice)-1][2]=="Chapter":
                    chapterInfo(result[int(choice)-1][1], conn)
                    break
            elif choice=="-1":
                return
            else:
                print("Wrong input, type again.")
    else:
        print("No match,  try again.\n")

def chapterInfo(title, conn):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT Distinct ch.Title , ch.DOI , ch.Abstract, p.Title, a.FirstName, a.LastName, Publisher.Name
                    FROM Chapter as ch, Scientific_Book as sb, (Publication as p join Composes as c on p.ID=c.PublicationID) join Author as a on a.ID=c.AuthorID, Publisher
                    WHERE ch.Title=? and ch.BookID=sb.ID AND p.ID=sb.ID and sb.PublisherID=Publisher.ID""", (title,))
    result=cursor.fetchall()
    print("The chapter {} is part of: {}\n".format(result[0][0], result[0][3]))
    print("DOI:{}".format(result[0][1]))
    print("Publisher:{}".format(result[0][6]))
    while(True):
        abstr=input("Do you want to show Chapter's Abstract?(Yes/No)\n")
        if abstr.lower()=="Yes": 
            print(result[0][2])
            break
        elif abstr.lower()=="No": 
            break
        else:
            print("Wrong input, type again")
    
    
    while(True):
        auth=input("Do you want to show chapter's authors?(Yes/No)\n")
        if auth=="Yes": 
            for i in range(len(result)):
                print("{} ".format(i+1),result[i][4], result[i][5])
            while(True):
                pr=input("If you want to show an author's profile press the number next to him.\n Else press -1.\n")
                if int(pr)>0 and int(pr)<=len(result):
                    AuthorProfile(result[int(pr)-1][4], result[int(pr)-1][5], conn)
                elif pr=="-1": 
                    break
                else:
                    print("Wrong input, type again")    
                break
            break
        elif auth=="No": 
            break
        else:
            print("Wrong input, type again")
    
def makechoice(conn):
    while (True):
        print("What do you want to search for?")
        choice=input("Press 1 for Author \nPress 2 for Title \nPress 3 for general search of keyword \nPress -1 to exit\n")
        match choice:
            case "1":
                flag=True
                while(True):
                    name=input("Type the author you are looking for. Or type <<back>> to go back\n")
                    if name.lower()=="back": break
                    searchforAuthor(name, conn, flag)

            case "2":
                flag=False
                while(True):
                    title=input("Type the Title you are looking for. Or type <<back>> to go back\n")
                    if title.lower()=="back": break
                    searchforTitle(title, conn, flag)
            case "3":
                flag=False
                while(True):
                    keyword=input("Type the keyword you are looking for. Or type <<back>> to go back\n")
                    if keyword.lower()=="back": break
                    searchforKeyword(keyword, conn, flag)
            case "-1":break
            case other:
                print("Wrong input type again.")

if __name__=="__main__":
    conn=sqlite3.connect('Scientific_Libary.db')

    print("Connected to SQLite")
    
    makechoice(conn)

    conn.close()