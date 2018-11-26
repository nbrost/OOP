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
                    ads = comparisonSearch(userInput,index)
                    #Call comparison search function(s) here
                    #have it return an array of the relevant aids 
                    
                    pass
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
def comparisonSearch(userInput,index):
    adIds = ()
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
    return ()

def catSearch(userInput, index):
    print('hey there')
    global dates_database
    global dates_cursor
    return()

def dateSearch(userInput,index):
    print('date ssearch')
    global dates_database
    global dates_cursor
    return()

def priceSearch(user_input,index):
    print('price')
    global price_database
    global price_cursor
    return()

main()