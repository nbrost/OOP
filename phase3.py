import re
from bsddb3 import db

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

fullOutput = False #True: print full output, False: print brief output

def main():
    getInput()
    terms_database.close()
    date_database.close()
    ad_database.close()
    price_database.close()
    print("\nGoodbye!")


''' Takes an array of aids and prints out the information of each.
    It prints out the full information if fullOutput is True, otherwise
    it prints out a brief report.'''
def printAds(aids):
    global fullOutput
    for aid in aids:
        #get title
        title = None
        #print aid, title
        print("\n\tAd Id:", aid)
        print("\tTitle:", title)
        
        if fullOutput:
            #get the values
            date = None
            loc = None
            cat = None
            price = None
            desc = None
            #print the values
            print("\tDate:")
            print("\tLocation:")
            print("\tCategory:")
            print("\tPrice: ")
            print("\tDescription:")


'''Takes the user's input and decides what to do with it. It's essentially a management function'''
def getInput():
    global fullOutput
    while True:
        userInput = input("\nEnter a query: ").lower()
        #aids is the array to hold the aids of the results returned by the searches
        aids = []
        
        #evaluates the user input
        if userInput == "q" or userInput == "quit":
            break
        elif userInput.startswith("output"):
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
        else:
            userInput = userInput.split(' ')
            for index in range(len(userInput)):
                if isComparison(userInput[index]):
                    compTuple = comparisonSearch(userInput,index, aids)
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
                    index += compTuple[1]
                    
                else:
                    
                    #Call term search function(s) here
                    #have it return an array of the relevant aids 
                    pass
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

def locationSearch(userInput,index):
    print ('hell')
    global dates_database
    global dates_cursor
    return None

def catSearch(userInput, index):
    print('hey there')
    global dates_database
    global dates_cursor
    return()

def dateSearch(user_input,index):
    offset = 0
    if '>=' in user_input[index]:
        user_input[index]=user_input[index].replace('>=','')
        if len(user_input[index]) >5:
            amount = (user_input[index][5:])            
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateGreater(amount)
        ids.append(dateEqual(amount))
        return(ids,offset)
    elif '<=' in user_input[index]:
        user_input[index] = user_input[index].replace('<=','')
        if len(user_input[index]) >5:
            amount = (user_input[index][5:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateLess(amount)
        ids.append(dateEqual(amount))
        return(ids,offset)
    elif '>' in user_input[index]:
        user_input[index]=user_input[index].replace('>','')
        if len(user_input[index]) >5:
            amount = (user_input[index][5:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateGreater(amount)
        return(ids,offset)
    elif '<' in user_input[index]:
        user_input[index] = user_input[index].replace('<','')
        if len(user_input[index]) >5:
            amount = (user_input[index][5:])
        else:
            amount = (user_input[index+1])
            offset = 1
        ids = dateLess(amount)
        return(ids,offset)  
    elif '=' in user_input[index]:
        user_input[index] = user_input[index].replace('=','')
        if len(user_input[index])>5:
            amount = (user_input[index][5:])
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
        ids.append(dateEqual(amount))
        return(ids,offset)
    elif '<=' in user_input[index +1]:
        if len(user_input[index+1])>2:
            amount = (user_input[index+1][2:])
            offset =1
        else:
            amount = (user_input[index+2])
            offset = 2
        ids = dateLess(amount)
        ids.append(dateEqual(amount))
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
    print(amount)
    global date_database
    global date_curs
    results = []
    date = amount
    date = date.encode('utf-8')
    idnum = date_curs.set_range(date)
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
        idnum = date_curs.next()
    
    return(results)
    
def dateLess(amount):
    pass
def dateEqual(amount):
    pass
def priceGreater(amount):
    
    global price_database
    global price_curs  
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