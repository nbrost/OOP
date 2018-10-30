import sqlite3
import time
import sys
import dbsetup
connection = None
cursor = None

#connects to the database
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

#clears the database
def drop_tables():
    global connection, cursor


    drop_requests = "drop table if exists requests;"
    drop_enroute = "drop table if exists enroute;"
    drop_bookings = "drop table if exists bookings;"
    drop_rides = "drop table if exists rides; "
    drop_locations = "drop table if exists locations;"
    drop_cars = "drop table if exists cars;"
    drop_members = "drop table if exists members;"
    drop_inbox = "drop table if exists inbox;"
    remove_keys = "PRAGMA foreign_keys=OFF"
    return_keys = "PRAGMA foreign_keys=ON;"
    cursor.execute(remove_keys)
    cursor.execute(drop_requests)
    cursor.execute(drop_enroute)
    cursor.execute(drop_bookings)
    
    cursor.execute(drop_locations)
    cursor.execute(drop_cars)
    cursor.execute(drop_members)
    cursor.execute(drop_inbox)
    cursor.execute(drop_rides)
    cursor.execute(return_keys)


#takes a email and password and tries to log in
#returns the members info if one exists
def sign_in():
    global connection, cursor
    while True:
        user = input("Enter email or quit: ")
        if user == "quit":
            end()
        password = input("Enter Password: ")
        log_in_query = ('''
        select email, name, phone, pwd
        from members
        where email = '{0}' COLLATE NOCASE
        and pwd = '{1}' ; '''.format(user, password))
        cursor.execute(log_in_query)#checks if a user with email/password exists
        member = cursor.fetchall()#stores the members info in member
        
        if member != []: #opens unread mail and returns if member exists
            open_mail(member[0])
            return member[0]
        #if member doesn't exist prints this and tries again
        print("Please enter a valid email/password combo or quit") 

#will display all unread mail and set them to read
def open_mail(member):
    global connection, cursor
    mail_query = ('''
    select content
    from  inbox
    where inbox.email = '{0}' COLLATE NOCASE
    and inbox.seen = 'n';'''.format(member[0]))
    cursor.execute(mail_query) #finds all unread mail for that user
    mail = cursor.fetchall()
    for i in range(len(mail)): #prints each unread email and sets them to read
        message = mail[i][0]
        print (("\nUnread email {0}: ").format(i+1))
        print (message)
        mail_query2 = ('''
        update inbox 
        set seen = 'y' 
        where email = '{0}' COLLATE NOCASE
        and content = '{1}';'''.format(member[0],message))
        cursor.execute(mail_query2)
    return


#creates a new user and stores it in the database
def create_user():
    global connection,cursor
    while True:
        email = input("Enter your email or cancel: ")
        if email == 'cancel':
            return
        email_query = ('''
        select email
        from members
        where email = '{0}' COLLATE NOCASE;'''.format(email))
        cursor.execute(email_query) # will see if any users already use the email
        test = cursor.fetchall()
        if test != []:#if the query isn't empty then the email is not unique
            print ("There is already a member with that email\nPlease provide a unique email")
        else:
            name = input("Enter your name: ") #gets info for a new user
            phone = input("Enter your phone number: ")
            password = input("Enter your password: ")
            new_member_query = ('''
            insert into members values
            ('{0}', '{1}', '{2}', '{3}');'''.format(email,name,phone,password))
            cursor.execute(new_member_query)#inserts the new user into members
            return

#this funtion starts out the code
#will ask whether signing in, creating a user or quiting
#if creating a user it will then ask you to sign into that user
def sign_in_screen():        
    while True:
        try:
            sign_in_flag = int(input("Press 1 to sign in, 2 to create a new user or 3 to quit: "))
            if sign_in_flag not in (1,2,3):
                print ("Please enter 1, 2 or 3")
        except:
            print ("Please enter 1, 2 or 3")   
        if sign_in_flag ==1:
            member = sign_in()
            return member
        elif sign_in_flag == 2:
            create_user()
        elif sign_in_flag == 3:
            end()



#this function is passed a member tuple that contains (email,name,phone,pwd)
#this will ask what the user wants to do 
def operations(member):
    option = input('''The following are your options:
    1.Offer Ride
    2.Search For Ride
    3.Book Members or Cancel Booking
    4.Post Ride Requests
    5.Search and Delete Ride Requests
    6.Log out
    7.Exit Program
    Please enter number: ''')
    try:
        option=int(option)
    except:
        print("Please enter 1-7")
        return
    if option == 1:
        offer_ride(member)
    elif option == 2:
        search_for_ride(member)
    elif option == 3:
        book_member(member)
    elif option == 4:
        post_request(member)
    elif option == 5:
        search_requests(member)
    elif option == 6:
        member = sign_in_screen()
    elif option == 7: 
        end()
    else:
        print("Please enter 1-7")
    return member
            
            
            
#prints goodbye and exits
def end():
    print("Goodbye")
    sys.exit()
    
    
def main():
    global connection, cursor
    
    path = "./rideshare.db"
    connect(path)
    drop_tables()
    dbsetup.define_tables(connection,cursor)
    dbsetup.insert_data(connection,cursor)
    member = sign_in_screen()
    while True:
        member = operations(member)
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
