import sqlite3

def book():
    bookTitle=input("Type the book's title.\n")
    bookAbstract=input("Type the book's abstract.\n")
    publicationYear=input("Year of publication.\n")
    #inserting Publication's information
    publ_sql='''INSERT INTO Publication(Title, Abstract,  Year)
            VALUES(?,?,?)'''
    cur=conn.cursor()
    cur.execute(publ_sql,(bookTitle,bookAbstract,publicationYear))
    conn.commit()

    publicationID=findPublicationID(bookTitle)
    
    #checking if the publisher already exists in database and if he doesn't i add him
    publisherName=input("Type the publisher's name.\n")
    publisherID=findPublisherID(publisherName)
    print(publisherID)
    if len(publisherID)==0:
        pub_sql='''INSERT INTO Publisher(Name)
            VALUES(?)'''
        cur.execute(pub_sql,(publisherName,))
        conn.commit()

        publisherID=findPublisherID(publisherName)

    bookType=input("Type the book's type.\n")
    persistentLink=input("Type the book's persistent link.\n")
    electronic_pdf_ISBN=input("Type the book's electronic pdf ISBN if it has one.(Else press enter)\n")
    if electronic_pdf_ISBN=="": electronic_pdf_ISBN=None
    electronic_epub_ISBN=input("Type the book's electronic epub ISBN if it has one.(Else press enter)\n")
    if electronic_epub_ISBN=="": electronic_epub_ISBN=None
    online_ISBN=input("Type the book's Online ISBN if it has one.(Else press enter)\n")
    if online_ISBN=="":online_ISBN=None
    print_ISBN=input("Type the book's print ISBN if it has one.(Else press enter)\n")
    if print_ISBN=="":print_ISBN=None

    sb_sql='''INSERT INTO Scientific_Book(ID, PublisherID, [Book Type], [Persistent Link], [Electronic pdf ISBN], [Electronic epub ISBN], [Online ISBN], [Print ISBN])
            VALUES(?,?,?,?,?,?,?,?)'''
    cur.execute(sb_sql,(int(publicationID[0][0]), int(publisherID[0][0]), bookType, persistentLink, electronic_pdf_ISBN, electronic_epub_ISBN, online_ISBN, print_ISBN))
    conn.commit()

    chapter_number=int(input("How many chapters does the book have?\n"))

    for i in range(chapter_number):
        if(i==0):
            chapterTitle=input("Type the {}st chapter's title.\n".format(i+1))
            chapter_abstract=input("Type the {}st chapter's abstract.\n".format(i+1))
            chapterDOI=input("Type the {}st chapter's DOI.\n".format(i+1))
        elif(i==1):
            chapterTitle=input("Type the {}nd chapter's title.\n".format(i+1))
            chapter_abstract=input("Type the {}nd chapter's abstract.\n".format(i+1))
            chapterDOI=input("Type the {}nd chapter's DOI.\n".format(i+1))
        elif(i==2):
            chapterTitle=input("Type the {}rd chapter's title.\n".format(i+1))
            chapter_abstract=input("Type the {}rd chapter's abstract.\n".format(i+1))
            chapterDOI=input("Type the {}rd chapter's DOI.\n".format(i+1))
        else:
            chapterTitle=input("Type the {}th chapter's title.\n".format(i+1))
            chapter_abstract=input("Type the {}th chapter's abstract.\n".format(i+1))
            chapterDOI=input("Type the {}th chapter's DOI.\n".format(i+1))
        #add each chapter separately
        abstr_sql='''INSERT INTO Chapter(BookID, Title, Abstract, DOI)
                VALUES(?,?,?,?)'''
        
        cur.execute(abstr_sql,(int(publicationID[0][0]),chapterTitle,chapter_abstract,chapterDOI))
        conn.commit()

        keyword_option=input("Do you want to add keywords?(Yes/No)\n")
        while(True):
            if(keyword_option=="Yes"):
                keywords=input("Type the abstract's keywords.\n")
                keywords=keywords.split(",")
                for k in keywords:
                    key_sql='''INSERT INTO Chapter_Keywords(ID, Keywords)
                                VALUES(?,?)'''
                    chapterID=findChapterID(chapterTitle)
                    cur.execute(key_sql,(int(chapterID[0][0]),k))
                    conn.commit()
                keyword_option=input("Do you want to add another keyword?(Yes/No)\n")
            elif(keyword_option=="No"):
                break
            else:
                print("Wrong input, type again.\n")
                keyword_option=input()

    while (True):
        bookAuthor=input("Type the Author's first name and last name.\n")
        bookAuthor=bookAuthor.split()
        AuthorID=findAuthorID(bookAuthor)
        if len(AuthorID)==0:#checking if author is already in database by checking if there is an ID matching
            email=input("Author not in database, type author's mail(optional).\n")
            city=input("Type author's city.\n")
            affiliation=input("Type author's affiliation.\n")
            #if he is not in database i add him
            author_sql='''INSERT INTO Author(FirstName, LastName, Mail, City)
                    VALUES(?,?,?,?)'''

            cur.execute(author_sql,(bookAuthor[0], bookAuthor[1], email, city))
            conn.commit()
        else: affiliation=input("Type author's affiliation.\n")

        AuthorID=findAuthorID(bookAuthor)
        #and i add composes to the database for both cases
        author_sql='''INSERT INTO Composes(AuthorID, PublicationID, Affiliation)
                VALUES(?,?,?)'''

        cur.execute(author_sql,(int(AuthorID[0][0]), int(publicationID[0][0]), affiliation))
        conn.commit()
        #checking if the book has more than one authors
        co_authors=input("Does the book have other co-author?(Yes/No)\n")
        while (True):
            if(co_authors=="No"):
                break
            elif(co_authors=="Yes"):
                break
            else:
                co_authors=input("Wront input, type again.\n")
        if(co_authors=="No"):break

    print("Book import finished successfully.\n")

def article():
    ArticleTitle=input("Type the book's title.\n")
    ArticleAbstract=input("Type the book's abstract.\n")
    publicationYear=input("Year of publication.\n")
    #inserting Publication's information
    publ_sql='''INSERT INTO Publication(Title, Abstract,  Year)
            VALUES(?,?,?)'''
    cur=conn.cursor()
    cur.execute(publ_sql,(ArticleTitle,ArticleAbstract,publicationYear))
    conn.commit()

    publicationID=findPublicationID(ArticleTitle)
    
    #checking if the publisher already exists in database and if he doesn't i add him
    publisherName=input("Type the publisher's name.\n")
    publisherID=findPublisherID(publisherName)
    print(publisherID)

    if len(publisherID)==0:
        pub_sql='''INSERT INTO Publisher(Name)
            VALUES(?)'''
        cur.execute(pub_sql,(publisherName,))
        conn.commit()

        publisherID=findPublisherID(publisherName)
        
    ArticleDOI=input("Type the Article's DOI if it has one.(Else press enter)\n")
    if ArticleDOI=="":ArticleDOI=None
    print_ISSN=input("Type the Article's print ISSN if it has one.(Else press enter)\n")
    if print_ISSN=="":print_ISSN=None
    electronic_ISSN=input("Type the Article's electronic ISSN if it has one.(Else press enter)\n")
    if electronic_ISSN=="": electronic_ISSN=None
    online_ISSN=input("Type the Article's Online ISSN if it has one.(Else press enter)\n")
    if online_ISSN=="":online_ISSN=None
    articleConference=input("Type the Conference that the Article was published in, if it was published in a conference.(Else press enter)\n")
    if articleConference=="":articleConference=None
    scienceMagazine=input("Type the Science Magazine that the Article was published in, if it was published in a Science Magazine.(Else press enter)\n")
    if scienceMagazine=="":scienceMagazine=None

    sb_sql='''INSERT INTO Articel(ID, PublisherID, DOI, [Print ISSN], [Electronic ISSN], [Online ISSN], Conference, [Science Magazine])
            VALUES(?,?,?,?,?,?,?,?)'''
    cur.execute(sb_sql,(int(publicationID[0][0]), int(publisherID[0][0]), ArticleDOI, print_ISSN, electronic_ISSN, online_ISSN, articleConference, scienceMagazine))
    conn.commit()

    citation_option=input("Do you want to add citations?(Yes/No)\n")
    while(True):
        count=1
        if(citation_option=="Yes"):
            citation=input("Type the citation No{} of the article.\n".format(count))
            citation_year=input("Type the year of the citation.\n")
            key_sql='''INSERT INTO Article_Citations(ID, Citations, Year)
                        VALUES(?,?,?)'''
            cur.execute(key_sql,(int(publicationID[0][0]), citation, citation_year))
            conn.commit()
            citation_option=input("Do you want to add another citation?(Yes/No)\n")
        elif(citation_option=="No"):
            break
        else:
            print("Wrong input, type again.\n")
            citation_option=input()

    reference_option=input("Do you want to add references?(Yes/No)\n")
    while(True):
        count=1
        if(reference_option=="Yes"):
            reference=input("Type the reference No{} of the article.\n".format(count))
            reference_year=input("Type the year of the reference.\n")
            key_sql='''INSERT INTO Article_References(ID, References, Year)
                        VALUES(?,?,?)'''
            cur.execute(key_sql,(int(publicationID[0][0]), reference, reference_year))
            conn.commit()
            reference_option=input("Do you want to add another reference?(Yes/No)\n")
        elif(reference_option=="No"):
            break
        else:
            print("Wrong input, type again.\n")
            reference_option=input()

    keyword_option=input("Do you want to add keywords?(Yes/No)\n")
    while(True):
        if(keyword_option=="Yes"):
            keywords=input("Type the Articles's keywords.\n")
            keywords=keywords.split(",")
            for k in keywords:
                key_sql='''INSERT INTO Article_Keywords(ID, Keywords)
                            VALUES(?,?)'''
                publicationID=findPublicationID(ArticleTitle)
                cur.execute(key_sql,(int(publicationID[0][0]),k))
                conn.commit()
            keyword_option=input("Do you want to add another keyword?(Yes/No)\n")
        elif(keyword_option=="No"):
            break
        else:
            print("Wrong input, type again.\n")
            keyword_option=input()

    while (True):
        articleAuthor=input("Type the Author's first name and last name.\n")
        articleAuthor=articleAuthor.split()
        AuthorID=findAuthorID(articleAuthor)
        if len(AuthorID)==0:#checking if author is already in database by checking if there is an ID matching
            email=input("Author not in database, type author's mail(optional).\n")
            city=input("Type author's city.\n")
            affiliation=input("Type author's affiliation.\n")
            #if he is not in database i add him
            author_sql='''INSERT INTO Author(FirstName, LastName, Mail, City)
                    VALUES(?,?,?,?)'''

            cur.execute(author_sql,(articleAuthor[0], articleAuthor[1], email, city))
            conn.commit()
        else: affiliation=input("Type author's affiliation.\n")

        AuthorID=findAuthorID(articleAuthor)
        #and i add composes to the database for both cases
        author_sql='''INSERT INTO Composes(AuthorID, PublicationID, Affiliation)
                VALUES(?,?,?)'''

        cur.execute(author_sql,(int(AuthorID[0][0]), int(publicationID[0][0]), affiliation))
        conn.commit()
        #checking if the book has more than one authors
        co_authors=input("Does the book have other co-author?(Yes/No)\n")
        while (True):
            if(co_authors=="No"):
                break
            elif(co_authors=="Yes"):
                break
            else:
                co_authors=input("Wront input, type again.\n")
        if(co_authors=="No"):break

    print("Article import finished successfully.\n")

def findAuthorID(author):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT a.ID
                    FROM Author as a
                    WHERE a.FirstName=? and a.LastName=?  """, (author[0],author[1]))
    result=cursor.fetchall()
    return result

def findChapterID(chapter):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT c.ID
                    FROM Chapter as c
                    WHERE c.Title=? """, (chapter,))
    result=cursor.fetchall()
    return result

def findPublisherID(publisher):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT p.ID
                    FROM Publisher as p
                    WHERE p.Name=? """, (publisher,))
    result=cursor.fetchall()
    
    return result

def findPublicationID(title):
    cursor = conn.cursor()
    # executing our sql query
    cursor.execute("""SELECT p.ID
                    FROM Publication as p
                    WHERE p.Title=? """, (title,))
    result=cursor.fetchall() 
    return result


        


def uploadchoice():
    while (True):
        print("What do you want to upload?")
        choice=input("Press 1 for Book \nPress 2 for Article \nPress -1 to exit\n")
        match choice:
            case "1":
                book()
            case "2":
                article()
            case "-1":
                quit()
            case other:
                print("Wrong input type again.")


conn=sqlite3.connect('Scientific_Libary.db')

print("Connected to SQLite")
 
uploadchoice()

conn.close()