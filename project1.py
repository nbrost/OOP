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
        input_test(user)
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
            name = input("Enter your name: ")
            input_test(name)#gets info for a new user
            while True:
                phone = input("Enter your phone number (XXX-XXX-XXXX): ")
                input_test(name)
                try:
                    assert(len(phone) == 12), ''    
                    int(phone[0:3]+phone[4:7] + phone[8:])
                    assert(phone[3] == '-' and phone[7] == '-'), ''
                    break
                except:
                    print("\nPlease enter a proper password.\n")
            
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
        sign_in_flag = (input("\nPlease select from the following options\n    1 to sign in\n    2 to create a new user: "))
        input_test(sign_in_flag)
        try:            
            sign_in_flag = int(sign_in_flag)
            if sign_in_flag not in (1,2):
                print ("Please enter 1 or 2")
        except:
            print ("Please enter 1 or 2")   
        if sign_in_flag ==1:
            member = sign_in()
            return member
        elif sign_in_flag == 2:
            create_user()


#This function will receive a member and ask for 1-3 location key words
#It will then query the database for rides that match all three queries
#It will display the first 5 with the option to see more
#The user will be given the option to send the ride poster a message to book the ride
def search_for_ride(member):
    global connection, cursor
    location1 = input("You are searching for rides\nPlease enter at least 1 Location\nEnter first location: ")
    input_test(location1)
    if location1 == '':
        return
    location2 = input("Enter second location: ")
    input_test(location2)
    location3 = location1
    if location2 !='':
        location3 = input("Enter third location: ")
        if location3 == '':
            location3 = location2
    else:
        location2 = location1
    input_test(location3)
    search_query = ('''
    select distinct rides.rno, rides.price, rides.rdate, rides.seats, rides.lugDesc,
                  rides.src, rides.dst, rides.driver, rides.cno
    from rides join locations as source on rides.src = source.lcode
               left join locations as destination on rides.dst = destination.lcode
               left join enroute on rides.rno = enroute.rno
               left join locations as enrou on enroute.lcode = enrou.lcode
    where (rides.src = '{0}' COLLATE NOCASE OR
           rides.dst = '{0}' COLLATE NOCASE OR
           source.city LIKE '%{0}%' COLLATE NOCASE OR
           source.prov LIKE '%{0}%' COLLATE NOCASE OR
           source.address LIKE '%{0}%' COLLATE NOCASE OR
           destination.city LIKE '%{0}%' COLLATE NOCASE OR
           destination.prov LIKE '%{0}%' COLLATE NOCASE OR 
           destination.address LIKE '%{0}%' COLLATE NOCASE OR
           enrou.city LIKE '%{0}%' COLLATE NOCASE OR
           enrou.prov LIKE '%{0}%' COLLATE NOCASE OR
           enrou.address LIKE '%{0}%' COLLATE NOCASE) AND
          (rides.src = '{1}' COLLATE NOCASE OR
           rides.dst = '{1}' COLLATE NOCASE OR
           source.city LIKE '%{1}%' COLLATE NOCASE OR
           source.prov LIKE '%{1}%' COLLATE NOCASE OR
           source.address LIKE '%{1}%' COLLATE NOCASE OR
           destination.city LIKE '%{1}%' COLLATE NOCASE OR
           destination.prov LIKE '%{1}%' COLLATE NOCASE OR 
           destination.address LIKE '%{1}%' COLLATE NOCASE OR
           enrou.city LIKE '%{1}%' COLLATE NOCASE OR
           enrou.prov LIKE '%{1}%' COLLATE NOCASE OR
           enrou.address LIKE '%{1}%' COLLATE NOCASE) AND 
          (rides.src = '{2}' COLLATE NOCASE OR
           rides.dst = '{2}' COLLATE NOCASE OR
           source.city LIKE '%{2}%' COLLATE NOCASE OR
           source.prov LIKE '%{2}%' COLLATE NOCASE OR
           source.address LIKE '%{2}%' COLLATE NOCASE OR
           destination.city LIKE '%{2}%' COLLATE NOCASE OR
           destination.prov LIKE '%{2}%' COLLATE NOCASE OR 
           destination.address LIKE '%{2}%' COLLATE NOCASE OR
           enrou.city LIKE '%{2}%' COLLATE NOCASE OR
           enrou.prov LIKE '%{2}%' COLLATE NOCASE OR
           enrou.address LIKE '%{2}%' COLLATE NOCASE);
               '''.format(location1,location2,location3))
    cursor.execute(search_query)
    rides = cursor.fetchall()
    if rides == []:
        print("Sorry but no rides matched your keywords")

    selected = print_rides(rides) #will print rides and ask for ride to message
    message_driver(selected, member)
    return

#checks to see if a ride exists and will send the driver a message if it does
def message_driver(rno, member):
    global connection, cursor
    message_query = """select driver
                       from rides
                       where rno = '{0}'""".format(rno)
    cursor.execute(message_query)
    address = cursor.fetchall()
    if address== []:
        print("Sorry that ride doesn't exist")
        return
    message = input("What would you like to say: ")
    input_test(message)
    send_message = """insert into inbox values ('{0}',datetime('now'),'{1}','{2}','{3}','n');""".format(
        address[0][0], member[0], message, rno)
    cursor.execute(send_message)
    print("\nMessage Sent!\n")
    return

#checks to see if a ride exists and will send the driver a message if it does
def message_requester(rid, member):
    global connection, cursor
    message_query = """select email
                       from requests
                       where rid = '{0}'""".format(rid)
    cursor.execute(message_query)
    address = cursor.fetchall()
    if address== []:
        print("Sorry that request doesn't exist")
        return
    message = input("What would you like to say: ")
    input_test(message)
    send_message = """insert into inbox values ('{0}',datetime('now'),'{1}','{2}','{3}','n');""".format(
        address[0][0], member[0], message, rid)
    cursor.execute(send_message)
    print("\nMessage Sent!\n")
    return




#Will print all rides 5 at a time and ask for the ride they wish to message about
#returns the ride number
def print_rides(rides):
    current = 0
    max = len(rides)
    for x in range(max):
        if rides[x][8] == None:
            ride_string =( '''\n\tRno: {0}\n\tPrice: {1}\n\tRide Date: {2}\n\tSeats: {3}\n\tLuggage Description:{4}
            Source code: {5}\n\tDestination Code {6}\n\tDriver: {7}\n\tCar Number: No car on Record'''.format(rides[x][0],
            rides[x][1], rides[x][2], rides[x][3], rides[x][4], rides[x][5], rides[x][6], rides[x][7]))
            print(ride_string)
        else:
            query = '''select * from cars where cno = {0};'''.format(rides[x][8])
            cursor.execute(query)
            cars = cursor.fetchall()
            ride_string =( '''\n\tRno: {0}\n\tPrice: {1}\n\tRide Date: {2}\n\tSeats: {3}\n\tLuggage Description:{4}Source code: {5}\n\tDestination Code {6}\n\tDriver: {7}\n\tCar Number: {8}\n\tMake: {9} Model: {10}\n\tYear: {11}\n\tSeats: {12}\n\tOwner: {13}'''.format(rides[x][0],rides[x][1], rides[x][2], rides[x][3], rides[x][4], rides[x][5], rides[x][6], rides[x][7], rides[x][8], cars[0][1], cars[0][2],
            cars[0][3], cars[0][4], cars[0][5]))
            print(ride_string)
        if ((x+1)%5 ==0):
            flag = input("\nContinue printing? (Y/N): ")
            input_test(flag)
            if flag in('No', 'N', 'NO', 'no', 'n'):
                break
    while(True):
        selected = input("Select ride number if you wish to message the driver: ")
        input_test(selected)
        if selected == '':
           return
        try:
            int(selected)
            return(selected)
        except:
            print("Sorry that is not a valid number")

#tests input to see if it is a quit string
def input_test(string):
    if string.lower() in ('q','quit'):
        end()
    return

#asks user for date, pickup location, drop off location, and amount willing to pay for seat
#will then post a ride request with a unique number and the members email address
def post_request(member):
    global connection, cursor
    while True:
        try:
            year = input("To request a ride please enter the following\n\tYear: ")
            assert (int(year) >=2018), ''
            month = input("\tMonth: ")
            assert (int(month) >0 and int(month) <13), ''
            if len(month) <2:
                month = '0' + month
            day = input('\tDay: ')
            assert (int(day) >0 and int(day) <32), ''
            if len(day) <2:
                day = '0' + day
            date = year + '-' + month + '-' + day # formats the data correctly
            break
        except:
            print("Please enter a correct date")
    pick_up = input("\tPick up location code: ")
    input_test(pick_up)
    drop_off = input("\tDrop off location code: ")
    input_test(drop_off)
    while True:
        try:
            price = input("\tAmount willing to pay: ")
            input_test(price)
            assert int(price) >0, ''
            break
        except:
            print('\tPlease enter a positive number')
    if not check_lcode(pick_up):
        print("\n Sorry That pick up location doesn't exist\n")
        return
    if not check_lcode(drop_off):
        print("\n Sorry that drop off location doesn't exist\n")
        return

    request_query = '''select rid
                       from requests
                       order by rid DESC
                       limit 1;'''
    cursor.execute(request_query) #gets the highest rno from the rides column
    rid = int((cursor.fetchall())[0][0]) + 1 #sets the rno to 1 greater than previous highest
    insert_query = '''insert into requests values (
                      {0},'{1}','{2}','{3}','{4}',{5});'''.format(rid, member[0], date, pick_up, drop_off, price)
    cursor.execute(insert_query)
    print("\nYour ride request has been posted\n")

    return


#will return true if a given lcode is in the database or False if it isn't
def check_lcode(lcode):
    global connection, cursor
    lcodes_query = '''select lcode
                    from locations
                    where lcode = '{0}';'''.format(lcode)

    cursor.execute(lcodes_query)
    pick_up = cursor.fetchall()
    if pick_up == []:
        return False
    return True


#will ask the member if they want to see their ride requests
#or if they want to search ride requests and message a member
def requests(member):
    global connection, cursor
    while True:
        option = input("Select from the following\n\tPress 1 to see your requests\n\tPress 2 to search requests: ")
        input_test(option)
        try:
            assert int(option) in (1,2), ''
            break
        except:
            print("Please select 1 or 2")
    if option == '1':
        display_requests(member)
        return
    search_requests(member)
    return

def search_requests(member):
    global connection, cursor
    location = input("\nEnter a location code or location: ")
    input_test(location)
    if location == '':
        return
    request_search = '''select r.rid, r.email, r.rdate, r.pickup, r.dropoff, r.amount
                        from requests as r 
                        left join locations as pickup on r.pickup = pickup.lcode
                        where (pickup.lcode = '{0}' OR
                               pickup.city LIKE '%{0}%' COLLATE NOCASE);'''.format(location)
    cursor.execute(request_search)
    requests = cursor.fetchall()
    if requests == []:
        print("\nSorry there aren't any requests that match your search\n")
        return
    print("\nThe following requests match your search\n")
    for x in range(len(requests)):
        requests_string = ('''\n\tRequest ID: {0}\n\tEmail: {1}\n\tRide Date: {2}\n\tPick up: {3}
        Drop off: {4}\n\tAmount: {5}\n''').format(requests[x][0], requests[x][1],
                                                    requests[x][2], requests[x][3],
                                                    requests[x][4], requests[x][5])
        print(requests_string)
        if ((x+1)%5 == 0):
            flag = input("\n Continue printing? (Y/N): ")
            input_test(flag)
            if flag in ('No', 'N', 'NO', 'no', 'n'):
                break
    rid = input("\nEnter Ride ID to message the requester: ")
    input_test(rid)
    if rid == '':
        return
    message_requester(rid, member)
    return


def display_requests(member):
    global connection, cursor
    request_query = '''select * from requests where email = '{0}';'''.format(member[0])
    cursor.execute(request_query)
    requests = cursor.fetchall()
    if requests == []:
        print("\nYou don't have any requests\n")
        return
    print("\nThe following are your requests\n")
    for x in range(len(requests)):
        requests_string = ('''\n\tRequest ID: {0}\n\tEmail: {1}\n\tRide Date: {2}\n\tPick up: {3}
        Drop off: {4}\n\tAmount: {5}\n''').format(requests[x][0], requests[x][1],
                                                    requests[x][2], requests[x][3],
                                                    requests[x][4], requests[x][5])
        print(requests_string)
        if ((x+1)%5 == 0):
            flag = input("\n Continue printing? (Y/N): ")
            input_test(flag)
            if flag in ('No', 'N', 'NO', 'no', 'n'):
                break
    drop_requests(member)
    return

def drop_requests(member):
    global connection, cursor
    while True:
        rid = input("\nEnter Ride Id of ride you wish to Delete: ")
        input_test(rid)
        if rid == '':
            return
        test_query = '''select * from requests where rid = '{0}' and email = '{1}';'''.format(rid,
                                                                                            member[0])
        cursor.execute(test_query)
        flag = cursor.fetchall()
        if flag ==[]:
            print("\nYou don't have any requests with that Ride Id")
        else:
            drop_query = '''delete from requests where rid = '{0}' and email = '{1}';'''.format(rid,
                                                                                            member[0])
            cursor.execute(drop_query)
            print('\nRide was successfully dropped\n')







#this function is passed a member tuple that contains (email,name,phone,pwd)
#this will ask what the user wants to do 
def operations(member):
    
    option = input('''\nThe following are your options:
    1.Offer Ride
    2.Search For Ride
    3.Book Members or Cancel Booking
    4.Post Ride Requests
    5.Search or Delete Ride Requests
    6.Log out
    7.Exit Program
    Please enter number: ''')
    input_test(option)
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
        requests(member)
    elif option == 6:
        member = sign_in_screen()
    elif option == 7:
        end()
    else:
        print("Please enter 1-7")
    return member
            
            
            
#prints goodbye and exits
def end():
    connection.commit()
    connection.close()
    print("Goodbye")
    sys.exit()
    
    
def main():
    global connection, cursor
    print("\nType q or quit at anytime to exit.\n")
    path = input ("Enter Database name: ")
    connect(path)
    #drop_tables()
    #dbsetup.define_tables(connection,cursor)
    #dbsetup.insert_data(connection,cursor)
    member = sign_in_screen()
    
    while True:
        member = operations(member)
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
