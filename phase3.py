import re

fullOutput = False #True: print full output, False: print brief output

def main():
    getInput()
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
            if isComparison(userInput):
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
    words = string.split()
    for word in words:
        if word in keywords:
            return True
    return False
    
    
main()