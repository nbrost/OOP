import re
from bsddb3 import db

fullOutput = False #True: print full output, False: print brief output
ads = None
terms = None
pdates = None
prices = None
#opens price index file
price_File = "pr.idx"
price_database = db.DB()
price_database.open(price_File,None, db.DB_BTREE, db.DB_RDONLY)
price_curs = price_database.cursor()

#opens date index file
date_File = "da.idx"
date_database = db.DB()
date_database.open(date_File,None, db.DB_BTREE, db.DB_RDONLY)
date_curs = date_database.cursor()

#opens ad index file
ad_File = "ad.idx"
ad_database = db.DB()
ad_database.open(ad_File,None, db.DB_HASH, db.DB_RDONLY)
ad_curs = ad_database.cursor()

#opens terms index file
terms_File = "te.idx"
terms_database = db.DB()
terms_database.open(terms_File,None, db.DB_BTREE, db.DB_RDONLY)
terms_curs = terms_database.cursor()
#cursor = None



def main():
    global database
    openDatabases()
    getInput()
    closeDatabases()
    
    print("\nGoodbye!")


def openDatabases():
    global ads, terms, pdates, prices
    ads = db.DB()
    ads.open("ad.idx")
    
    terms = db.DB()
    terms.open("te.idx")
    
    pdates = db.DB()
    pdates.open("da.idx")
    
    prices = db.DB()
    prices.open("pr.idx")

    
    
def closeDatabases():
    global ads, terms, pdates, prices
    ads.close()
    terms.close()
    pdates.close()
    prices.close()
    terms_database.close()
    date_database.close()
    ad_database.close()
    price_database.close()    


''' Takes an array of aids and prints out the information of each.
    It prints out the full information if fullOutput is True, otherwise
    it prints out a brief report.'''
def printAds(aids):
    global fullOutput, ads
    for aid in aids:
        try:
            aid = aid.encode('utf-8')
        except:
            pass
        try:
            #aid = bytes(aid.decode('utf-8')[0:-1], encoding='utf-8') #awkwardly removes the \n on aid
            line = ads.get(aid).decode('utf-8') #added ascii decoding here
        except:
            print("There was an error when printing.")
            return
        #get title
        title = re.search("<ti>"+"(.*)"+"</ti>", line).group(1)
        #print aid, title
        print("\n\tAd Id:", aid.decode('utf-8')) #added ascii decoding here
        print("\tTitle:", title)
        
        if fullOutput:
            #get the values
            date = re.search("<date>"+"(.*)"+"</date>", line).group(1)
            loc = re.search("<loc>"+"(.*)"+"</loc>", line).group(1)
            cat = re.search("<cat>"+"(.*)"+"</cat>", line).group(1)
            price = re.search("<price>"+"(.*)"+"</price>", line).group(1)
            desc = re.search("<desc>"+"(.*)"+"</desc>", line).group(1)
            #print the values
            print("\tDate:", date)
            print("\tLocation:", loc)
            print("\tCategory:", cat)
            print("\tPrice: ", price)
            print("\tDescription:", desc)



'''Takes the user's input and decides what to do with it. It's essentially a management function'''
def getInput():
    global fullOutput, ads, terms, pdates, prices
    while True:
        userInput = input("\nEnter a query: ").lower()
        indexBump = 0
        aids = []
        
        #evaluates the user input
        if userInput == "q" or userInput == "quit":
            break
        elif userInput.startswith("output"): #allows output to be passed to term/comparison search if it's a substring
            values = userInput.replace(" ", "").split("=")
            if len(values) == 2:
                val = values[1]
                if val == "full":
                    fullOutput = True
                elif val == "brief":
                    fullOutput = False
                else:
                    print("Invalid request.")
            else:
                print("Invalid request.")
        elif len(userInput) > 0:
            userInput = userInput.split(' ')
            for index in range(len(userInput)):
                if (index + indexBump) < len(userInput):
                    if isComparison(userInput[index+indexBump]):
                        compTuple = comparisonSearch(userInput,index+indexBump, aids)
                        #Call comparison search function(s) here
                        #have it return an array of the relevant aids 
                        if compTuple[0] == None:
                            print("No ads match that query")
                            break
                        deleting = []
                        if aids == []:
                            aids = compTuple[0]
                    
                        else:
                            for index in range(len(aids)):
                                if aids[index] not in compTuple[0]: 
                                    deleting.append(index)
                        deleting.reverse()
                        if deleting != []:
                            for i in deleting:
                                del aids[i]
                        indexBump += compTuple[1]

                    else:
                        index = index+indexBump
                        deleting = []
                        if aids == []:
                            aids = termSearch(userInput[index])
                        else:
                            idTuple = termSearch(userInput[index])
                            for index in range(len(aids)):
                                if aids[index] not in idTuple:
                                    deleting.append(index)
                        deleting.reverse()
                        if deleting!=[]:
                            for i in deleting:
                                del aids[i]
        
        if aids != []:
            printAds(aids)


'''Checks to see if the given string contains any of the keywords'''
def isComparison(string):
    keywords = ["price", "cat", "location", "date"]
    for word in keywords:
        if word in string:
            if len(string)>=8:
                if string[0:8] == 'location':
                    return True
                if string[0:5] == 'price':
                    return True
                if string[0:4] == 'date' :
                    return True
                if string[0:3] == 'cat':
                    return True
            elif len(string)>=5:
                if string[0:5] == 'price':
                    return True
                if string[0:4] == 'date' :
                    return True
                if string[0:3] == 'cat':
                    return True
            elif len(string)>=4:
                if string[0:4] == 'date' :
                    return True
                if string[0:3] == 'cat':
                    return True
            elif len(string)>=3:
                if string[0:3] == 'cat':
                    return True
    return False
#determines which type of search to do and calls appropriate function
def comparisonSearch(userInput,index,prevIds):
    adIds = () #will be a tuple where [0] = tuple of ids [1] = offset
    if len(userInput[index])>=8:
        if userInput[index][0:8] == 'location':
            adIds = locationSearch(userInput,index)
        if userInput[index][0:5] == 'price':
            adIds = priceSearch(userInput,index)
        if userInput[index][0:4] == 'date' :
            adIds = dateSearch(userInput,index)
        if userInput[index][0:3] == 'cat':
            adIds = catSearch(userInput, index)
    elif len(userInput[index])>=5:
        if userInput[index][0:5] == 'price':
            adIds = priceSearch(userInput,index)
        if userInput[index][0:4] == 'date' :
            adIds = dateSearch(userInput,index)
        if userInput[index][0:3] == 'cat':
            adIds = catSearch(userInput, index)
    elif len(userInput[index])>=4:
        if userInput[index][0:4] == 'date' :
            adIds = dateSearch(userInput,index)
        if userInput[index][0:3] == 'cat':
            adIds = catSearch(userInput, index)
    elif len(userInput[index])>=3:
        if userInput[index][0:3] == 'cat':
            adIds = catSearch(userInput, index)
    return adIds


'''Takes the a string and searches for matches in the terms file'''
def termSearch(term):
    global terms 
    cursor = terms.cursor()
    L = []
    term = term.replace(" ", "")
    if validTerm(term):
        if term.endswith("%"):
            term = term[0:-1]
            result = cursor.set_range(bytes(term, encoding="utf-8")) #added ascii decoding here
            while result != None and result[0].decode('utf-8').startswith(term): #added ascii decoding here
                if result[1] not in L: 
                    L.append(result[1].decode('utf-8'))
                result = cursor.next()
            if L == []:
                print("No results returned <"+term+">")
        else:
            result = cursor.set_range(bytes(term, encoding="utf-8")) #added ascii decoding here
            while result != None and result[0].decode('utf-8') == term: #added ascii decoding here
                if result[1] not in L: 
                    L.append(result[1].decode('utf-8'))
                result = cursor.next()
            if L == []:
                print("No results returned <"+term+">")            
    else:
        print("Invalid term:", term)
    cursor.close()
    return L

#checks the validity of a given term
#assumes that, excluding a valid wildcard symbol, the term must be more than 2 characters
def validTerm(term):
    length = len(term)
    if term.endswith("%"):
            if length>3:
                for i in range(length-1):
                    if re.match("[0-9a-zA-Z_-]", term[i]) == None:
                        print("Invalid term.")
                        return False               
            else:
                print("Invalid term.")
                return False
    elif length > 2:
        for i in range(length): 
            if re.match("[0-9a-zA-Z_-]", term[i]) == None:
                print("Invalid term.")
                return False
    else:
        print("Invalid term.")
        return False
    return True
def locationSearch(userInput,index):
    offset = 0
    if len(userInput[index]) >9:
        offset= 0
        location = userInput[index][9:]
    elif len(userInput[index]) == 9:
        offset = 1
        location = userInput[index+1]
    else:
        if len(userInput[index+1]) == 1:
            offset = 2
            location = userInput[index+2]
        else:
            offset = 1
            location = userInput[index+1][1:]
    ids = locationEqual(location)
    return (ids,offset)

def locationEqual(location):
    global price_curs, price_database
    iter = price_curs.first()
    ads = []
    while (iter):
        loc= iter[1].decode('utf-8')
        loc= loc.split(',')
        loc = loc[-1].lower()
        if loc == location.lower():
            aid = iter[1].decode('utf-8')
            aid = aid.split(',')
            aid = aid[0]
            ads.append(aid)        
    
        #iterating through duplicates
        dup = price_curs.next_dup()
        while(dup!=None):
            loc = dup[1].decode('utf-8')
            loc = loc.split(',')
            loc = loc[-1].lower()
            if loc == location.lower():
                aid = dup[1].decode('utf-8')
                aid = aid.split(',')
                aid = aid[0]
                ads.append(aid)
            dup = price_curs.next_dup()
    
        iter = price_curs.next()
    return(ads)
    

def catSearch(userInput, index):
    print('hey there')
    global dates_database
    global dates_cursor
    return()

def dateSearch(user_input,index):
    offset = 0
    if '>=' in user_input[index]:
        user_input[index]=user_input[index].replace('>=','')
        if len(user_input[index]) >4:
            amount = (user_input[index][4:])            
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateGreater(amount)
        if ids == None:
            ids = []
        equalids = dateEqual(amount)
        if equalids!=None:
            for i in range(len(equalids)):
                if equalids[i] != None:
                    ids.append(equalids[i])
        if ids == []:
            ids = None
        return(ids,offset)
    elif '<=' in user_input[index]:
        user_input[index] = user_input[index].replace('<=','')
        if len(user_input[index]) >4:
            amount = (user_input[index][4:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateLess(amount)
        if ids == None:
            ids = []
        equalids = dateEqual(amount)
        if equalids != None:
            for i in range(len(equalids)):
                if equalids[i] != None:
                    ids.append(equalids[i])
        if ids == []:
            ids = None
        return(ids,offset)
    elif '>' in user_input[index]:
        user_input[index]=user_input[index].replace('>','')
        if len(user_input[index]) >4:
            amount = (user_input[index][4:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateGreater(amount)
        return(ids,offset)
    elif '<' in user_input[index]:
        user_input[index] = user_input[index].replace('<','')
        if len(user_input[index]) >4:
            amount = (user_input[index][4:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateLess(amount)
        return(ids,offset)  
    elif '=' in user_input[index]:
        user_input[index] = user_input[index].replace('=','')
        if len(user_input[index])>4:
            amount = (user_input[index][4:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateEqual(amount)
        return(ids,offset)
    elif '>=' in user_input[index+1]:
        if len(user_input[index+1])>2:
            amount = (user_input[index+1][2:])
            offset = 1
        else:
            amount = (user_input[index+2])
            offset = 2
        ids = dateGreater(amount)
        if ids == None:
            ids = []
        equalids = dateEqual(amount)
        if equalids != None:
            for i in range(len(equalids)):
                if equalids[i] != None:
                    ids.append(equalids[i])
        if ids == []:
            ids = None
        return(ids,offset)
    elif '<=' in user_input[index +1]:
        if len(user_input[index+1])>2:
            amount = (user_input[index+1][2:])
            offset =1
        else:
            amount = (user_input[index+2])
            offset = 2
        ids = dateLess(amount)
        if ids == None:
            ids = []
        equalids= dateEqual(amount)
        if equalids!= None:
            for i in range(len(equalids)):
                if equalids[i] != None:
                    ids.append(equalids[i])
        if ids == []:
            ids = None
        return(ids,offset)
    elif '>' in user_input[index+1]:
        if len(user_input[index+1])>1:
            amount = (user_input[index+1][1:])
            offset = 1
        else:
            amount = (user_input[index+2])
            offset = 2
        ids = dateGreater(amount)
        return(ids,offset) 
    elif '<' in user_input[index+1]:
        if len(user_input[index+1])>1:
            amount = (user_input[index+1][1:])
            offset = 1
        else:
            amount = (user_input[index+2])
            offset = 2
        ids = dateLess(amount)
        return(ids,offset)  
    elif '=' in user_input[index+1]:
        if len(user_input[index+1])>1:
            amount = (user_input[index+1][1:])
            offset = 1
        else:
            amount = (user_input[index+2])
            offset = 2
        ids = dateEqual(amount)
        return(ids,offset)    
    else:
        return(None,0)

def priceSearch(user_input,index):
    offset = 0
    if '>=' in user_input[index]:
        user_input[index]=user_input[index].replace('>=','')
        if len(user_input[index]) >5:
            amount = int(user_input[index][5:])            
        else:
            amount = int(user_input[index+1])
            offset = 1
        ids = priceGreater(amount-1)
        return(ids,offset)
    elif '<=' in user_input[index]:
        user_input[index] = user_input[index].replace('<=','')
        if len(user_input[index]) >5:
            amount = int(user_input[index][5:])
        else:
            amount = int(user_input[index+1])
            offset = 1
        ids = priceLess(amount +1)
        return(ids,offset)
    elif '>' in user_input[index]:
        user_input[index]=user_input[index].replace('>','')
        if len(user_input[index]) >5:
            amount = int(user_input[index][5:])
        else:
            amount = int(user_input[index+1])
            offset = 1
        ids = priceGreater(amount)
        return(ids,offset)
    elif '<' in user_input[index]:
        user_input[index] = user_input[index].replace('<','')
        if len(user_input[index]) >5:
            amount = int(user_input[index][5:])
        else:
            amount = int(user_input[index+1])
            offset = 1
        ids = priceLess(amount)
        return(ids,offset)  
    elif '=' in user_input[index]:
        user_input[index] = user_input[index].replace('=','')
        if len(user_input[index])>5:
            amount = int(user_input[index][5:])
        else:
            amount = int(user_input[index+1])
            offset = 1
        ids = priceEqual(amount)
        return(ids,offset)
    elif '>=' in user_input[index+1]:
        if len(user_input[index+1])>2:
            amount = int(user_input[index+1][2:])
            offset = 1
        else:
            amount = int(user_input[index+2])
            offset = 2
        ids = priceGreater(amount-1)
        return(ids,offset)
    elif '<=' in user_input[index +1]:
        if len(user_input[index+1])>2:
            amount = int(user_input[index+1][2:])
            offset =1
        else:
            amount = int(user_input[index+2])
            offset = 2
        ids = priceLess(amount+1)
        return(ids,offset)
    elif '>' in user_input[index+1]:
        if len(user_input[index+1])>1:
            amount = int(user_input[index+1][1:])
            offset = 1
        else:
            amount = int(user_input[index+2])
            offset = 2
        ids = priceGreater(amount)
        return(ids,offset) 
    elif '<' in user_input[index+1]:
        if len(user_input[index+1])>1:
            amount = int(user_input[index+1][1:])
            offset = 1
        else:
            amount = int(user_input[index+2])
            offset = 2
        ids = priceLess(amount)
        return(ids,offset)  
    elif '=' in user_input[index+1]:
        if len(user_input[index+1])>1:
            amount = int(user_input[index+1][1:])
            offset = 1
        else:
            amount = int(user_input[index+2])
            offset = 2
        ids = priceEqual(amount)
        return(ids,offset)    
    else:
        return(None,0)
    
def dateGreater(amount):
    global date_database
    global date_curs
    results = []
    date = amount
    day = int(amount[-2:])
    
    day+=1
    if day<10:
        day = '0' + str(day)
    else:
        day = str(day)
    date = date[0:-2] + day
    
    date = date.encode('utf-8')
    idnum = date_curs.set_range(date)
    if idnum == None:
        return None
    idnum = idnum[1].decode('utf-8')
    idnum = idnum.split(',')
    results.append(idnum[0])
    idnum=date_curs.next()
    while idnum!= None:
        idnum = idnum[1].decode('utf-8')
        idnum = idnum.split(',')
        results.append(idnum[0])
        idnum = date_curs.next()
    
    return(results)
    
def dateLess(amount):
    global date_database
    global date_curs 
    results = []
    date = amount.encode('utf-8')
    idnum = date_curs.set_range(b'0')
    if idnum == None:
        return None
    idnum = idnum[1].decode("utf-8")
    idnum = idnum.split(',')
    results.append(idnum[0])
    idnum = date_curs.next()
    while idnum!=None:
        idnum = ((idnum[0].decode("utf-8")),idnum[1])
        if idnum[0]>= amount:
            break
        idnum = idnum[1].decode("utf-8")
        idnum = idnum.split(',')
        results.append(idnum[0])
        idnum = date_curs.next()

    return(results)
def dateEqual(amount):
    global date_database
    global date_curs  
    date = amount
    date = date.encode("utf-8")
    results = []
    idnum = date_curs.set(date)
    if idnum == None:
        return None
    idnum = idnum[1].decode("utf-8")
    idnum = idnum.split(',')
    results.append(idnum[0])
    
    for i in range(date_curs.count()-1):
        idnum = date_curs.next_dup()[1].decode('utf-8')
        
        idnum=idnum.split(',')
        
        results.append(idnum[0])

    return(results)
def priceGreater(amount):
    
    global price_database
    global price_curs  
    amount +=1
    amount = str(amount)
    amount = '            ' + amount
    amount = amount[-12:]
    amount = amount.encode('utf-8')
    results = []
    idnum = price_curs.set_range(amount)
    if idnum == None:
        return None
    idnum = idnum[1].decode('utf-8')
    idnum = idnum.split(',')
    results.append(idnum[0])
    idnum=price_curs.next()
    while idnum!= None:
        idnum = idnum[1].decode('utf-8')
        idnum = idnum.split(',')
        results.append(idnum[0])
        idnum = price_curs.next()
    
    return(results)
def priceLess(amount):
    
    global price_database
    global price_curs 
    
    bamount = str(amount)
    bamount = '            '+ bamount
    bamount = bamount[-12:]
    bamount = bamount.encode("utf-8")
    results = []
    idnum = price_curs.set_range(b'           0')
    if idnum == None:
        return None
    idnum = idnum[1].decode("utf-8")
    idnum = idnum.split(',')
    results.append(idnum[0])
    idnum = price_curs.next()
    while idnum!=None:
        idnum = (int(idnum[0].decode("utf-8")),idnum[1])
        if idnum[0]>= amount:
            break
        idnum = idnum[1].decode("utf-8")
        idnum = idnum.split(',')
        results.append(idnum[0])
        idnum = price_curs.next()

    return(results)
def priceEqual(amount):
    global price_database
    global price_curs  
    amount = str(amount)
    amount = '            '+ amount
    amount = amount[-12:]
    amount = amount.encode("utf-8")
    results = []
    idnum = price_curs.set(amount)
    if idnum == None:
        return None
    idnum = idnum[1].decode("utf-8")
    idnum = idnum.split(',')
    results.append(idnum[0])
    
    for i in range(price_curs.count()-1):
        idnum = price_curs.next_dup()[1].decode('utf-8')
        
        idnum=idnum.split(',')
        
        results.append(idnum[0])

    return(results)    
main()