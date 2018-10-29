import sqlite3
import time
import sys
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

#sets the tables based on the given schemas
def define_tables():
    global connection, cursor

    members_query = '''
			create table members (
  			  email		char(15),
			  name		char(20),
			  phone		char(12),
			  pwd		char(6),
			  primary key (email)
			);
		    '''

    cars_query =    '''
			create table cars (
			  cno		int,
			  make		char(12),
			  model		char(12),
			  year		int,
			  seats		int,
			  owner		char(15),
			  primary key (cno),
			  foreign key (owner) references members
			);
		     '''

    locations_query= '''
			create table locations (
			  lcode		char(5),
			  city		char(16),
			  prov		char(16),
			  address	char(16),
			  primary key (lcode)
			);
		     '''
    rides_query =    '''
                        create table rides (
                          rno		        int,
                          price		int,
                          rdate		date,
                          seats		int,
                          lugDesc	char(10),
                          src		char(5),
                          dst		char(5),
                          driver	char(15),
                          cno		int,
                          primary key (rno),
                          foreign key (src) references locations,
                          foreign key (dst) references locations,
                          foreign key (driver) references members,
                          foreign key (cno) references cars
                        );
                      '''
    bookings_query =  '''
                        create table bookings (
                          bno		int,
                          email		char(15),
                          rno		int,
                          cost		int,
                          seats		int,
                          pickup	char(5),
                          dropoff	char(5),
                          primary key (bno),
                          foreign key (email) references members,
                          foreign key (rno) references rides,
                          foreign key (pickup) references locations,
                          foreign key (dropoff) references locations
                        );
                      '''
    enroute_query =   '''
                        create table enroute (
                          rno		int,
                          lcode		char(5),
                          primary key (rno,lcode),
                          foreign key (rno) references rides,  
                          foreign key (lcode) references locations
                        );
                      '''
    requests_query =  '''
                        create table requests (
                          rid		int,
                          email		char(15),
                          rdate		date,
                          pickup	char(5),
                          dropoff	char(5),
                          amount	int,
                          primary key (rid),
                          foreign key (email) references members,
                          foreign key (pickup) references locations,
                          foreign key (dropoff) references locations
                        );
                      '''
    inbox_query =     '''
                        create table inbox (
                          email		char(15),
                          msgTimestamp	date,
                          sender	char(15),
                          content	text,
                          rno		int,
                          seen		char(1),
                          primary key (email, msgTimestamp),
                          foreign key (email) references members,
                          foreign key (sender) references members,
                          foreign key (rno) references rides
                        );
                      '''
                     
    cursor.execute(members_query)
    cursor.execute(cars_query)
    cursor.execute(locations_query)
    cursor.execute(rides_query)
    cursor.execute(bookings_query)
    cursor.execute(enroute_query)
    cursor.execute(requests_query)
    cursor.execute(inbox_query)
    connection.commit()

    return

#inserts the data into the database
def insert_data():
    global connection, cursor

    insert_query = '''insert into members values 
        ('jane_doe@abc.ca', 'Jane Maria-Ann Doe', '780-342-7584', 'jpass'),
        ('bob@123.ca', 'Bob Williams', '780-342-2834', 'bpass'),
        ('maria@xyz.org', 'Maria Calzone', '780-382-3847', 'mpass'),
        ('the99@oil.com', 'Wayne Gretzky', '780-382-4382', 'tpass'),
        ('connor@oil.com', 'Connor Mcdavid', '587-839-2838', 'cpass'),
        ('don@mayor.yeg', 'Don Iveson', '780-382-8239', 'dpass'),
        ('darryl@oil.com', 'Darryl Katz', '604-238-2380', 'dpass'),
        ('reilly@esks.org', 'Mike Reilly', '780-389-8928', 'rpass'),
        ('mess@marky.mark', 'Mark Messier', '516-382-8939', 'mpass'),
        ('mal@serenity.ca', 'Nathan Fillion', '780-389-2899', 'mpass'),
        ('kd@lang.ca', 'K. D. Lang', '874-384-3890', 'kpass'),
        ('nellie@five.gov', 'Nellie McClung', '389-930-2839', 'npass'),
        ('marty@mc.fly', 'Micheal J. Fox', '780-382-3899', 'mpass'),
        ('cadence@rap.fm', 'Roland Pemberton', '780-938-2738', 'cpass'),
        ('john@acorn.nut', 'John Acorn', '780-389-8392', 'jpass');
                
-- |cno|make|model|year|seats|owner|
insert into cars values 
        (1, 'Honda', 'Civic', 2010, 4, 'jane_doe@abc.ca'),
        (2, 'Ford', 'E-350', 2012, 15, 'bob@123.ca'),
        (3, 'Toyota', 'Rav-4', 2016, 4, 'don@mayor.yeg'),
        (4, 'Subaru', 'Forester', 2017, 4, 'reilly@esks.org'),
        (5, 'Ford', 'F-150', 2018, 4, 'connor@oil.com'),
        (6, 'Ram', '2500', 2017, 4, 'mess@marky.mark'),
        (7, 'Toyota', 'Matrix', 2007, 4, 'maria@xyz.org'),
        (8, 'Dodge', 'Caravan', 2013, 6, 'mess@marky.mark'),
        (9, 'Ford', 'Flex', 2011, 4, 'maria@xyz.org'),
        (10, 'Volkswagon', 'Vanagon', 1974, 5, 'the99@oil.com'),
        (11, 'Toyota', 'Sienna', 2012, 6, 'john@acorn.nut'),
        (12, 'Honda', 'Accord', 2010, 4, 'john@acorn.nut'),
        (13, 'Jeep', 'Wrangler', 2007, 2, 'cadence@rap.fm');

-- |lcode|city|prov|address|
insert into locations values
        ('cntr1', 'Edmonton', 'Alberta', 'Rogers Place'),
        ('cntr2', 'Edmonton', 'Alberta', 'City Hall'),
        ('sth1', 'Edmonton', 'Alberta', 'Southgate'),
        ('west1', 'Edmonton', 'Alberta', 'West Ed Mall'),
        ('cntr3', 'Edmonton', 'Alberta', 'Tyrell Museum'),
        ('cntr4', 'Edmonton', 'Alberta', 'Citadel Theater'),
        ('cntr5', 'Edmonton', 'Alberta', 'Shaw Center'),
        ('sth2', 'Edmonton', 'Alberta', 'Black Dog'),
        ('sth3', 'Edmonton', 'Alberta', 'The Rec Room'),
        ('sth4', 'Edmonton', 'Alberta', 'MEC South'),
        ('nrth1', 'Edmonton', 'Alberta', 'MEC North'),
        ('nrth2', 'Edmonton', 'Alberta', 'Rexall Place'),
        ('nrth3', 'Edmonton', 'Alberta', 'Commonwealth'),
        ('nrth4', 'Edmonton', 'Alberta', 'Northlands'),
        ('yyc1', 'Calgary', 'Alberta', 'Saddledome'),
        ('yyc2', 'Calgary', 'Alberta', 'McMahon Stadium'),
        ('yyc3', 'Calgary', 'Alberta', 'Calgary Tower'),
        ('van1', 'Vancouver', 'British Columbia', 'BC Place'),
        ('van2', 'Vancouver', 'British Columbia', 'Rogers Arena'),
        ('sk1', 'Regina', 'Saskatchewan', 'Mosaic Field'),
        ('sk2', 'Saskatoon', 'Saskatchewan', 'Wanuskewin'),
        ('ab1', 'Jasper', 'Alberta', 'Jasper Park Lodge');
        --('van3', 'Abbotsford', 'British Columbia', 'Abbotsford Airport');

-- |rno|price|rdate|seats|lugDesc|src|dst|driver|cno|
insert into rides values
        (1, 50, '2018-11-01', 4, 'Large Bag', 'cntr1', 'yyc1', 'the99@oil.com', 10),
        (2, 50, '2018-11-05', 4, 'Large Bag', 'yyc1', 'cntr2', 'the99@oil.com', 10),
        (3, 50, '2018-11-30', 4, 'Medium Bag', 'cntr1', 'yyc1', 'mess@marky.mark', 8),
        (4, 30, '2018-11-17', 15, '5 large bags', 'nrth1', 'yyc2', 'bob@123.ca', 2),
        (5, 50, '2018-11-23', 3, 'Backpack', 'cntr2', 'yyc3', 'maria@xyz.org', 7),
        (6, 10, '2018-07-23', 4, 'Medium Bag', 'west1', 'sth4', 'don@mayor.yeg', 3),
        (7, 10, '2018-09-30', 4, 'Medium Bag', 'cntr2', 'cntr3', 'reilly@esks.org', 4),
        (8, 10, '2018-10-11', 4, 'Medium Bag', 'nrth1', 'sth2', 'connor@oil.com', 4),
        (9, 10, '2018-10-12', 4, 'Medium Bag', 'cntr5', 'sth3', 'jane_doe@abc.ca', 1),
        (10, 10, '2018-04-26', 4, 'Medium Bag', 'cntr4', 'cntr2', 'bob@123.ca', 2),
        (11, 100, '2018-08-08', 4, 'Medium Bag', 'cntr1', 'van1', 'mess@marky.mark', 6),
        (12, 100, '2018-05-13', 2, 'Medium Bag', 'sk1', 'van2', 'bob@123.ca', 2),
        (13, 75, '2018-06-11', 3, 'Large Bag', 'yyc1', 'sk2', 'the99@oil.com', 10),
        (14, 10, '2018-10-13', 4, 'Large Bag', 'sth4', 'yyc1', 'reilly@esks.org', 4),
        (15, 15, '2018-10-05', 5, 'Medium Bag', 'nrth4', 'yyc1', 'the99@oil.com', 10),
        (16, 75, '2018-10-03', 2, 'Small Bag', 'yyc3', 'sk2', 'connor@oil.com', 5),
        (17, 150, '2018-10-11', 3, 'Medium Bag', 'sk2', 'van1', 'jane_doe@abc.ca', 1),
        (18, 10, '2018-10-23', 3, 'Large Bag', 'nrth3', 'yyc1', 'don@mayor.yeg', 3),
        (19, 10, '2015-04-22', 4, 'Small Bag', 'cntr1', 'cntr2', 'bob@123.ca', 2),
        (20, 50, '2018-12-11', 1, 'Large Bag', 'cntr2', 'yyc2', 'the99@oil.com', 10),
        (21, 50, '2018-12-12', 1, 'Large Bag', 'cntr2', 'yyc3', 'the99@oil.com', 10),
        (22, 10, '2018-09-13', 1, 'Large Bag', 'cntr2', 'cntr4', 'the99@oil.com', 10),
        (23, 10, '2018-09-14', 1, 'Large Bag', 'cntr2', 'cntr5', 'the99@oil.com', 10),
        (24, 10, '2018-09-15', 1, 'Large Bag', 'cntr2', 'sth1', 'the99@oil.com', 10),
        (25, 10, '2018-09-16', 1, 'Large Bag', 'cntr2', 'sth2', 'the99@oil.com', 10),
        (26, 50, '2018-12-06', 1, 'Large Bag', 'cntr2', 'yyc1', 'bob@123.ca', 2),
        (27, 53, '2018-09-07', 2, 'Large Bag', 'cntr2', 'yyc3', 'bob@123.ca', 2),
        (28, 10, '2018-09-08', 1, 'Large Bag', 'cntr2', 'cntr4', 'bob@123.ca', 2),
        (29, 10, '2018-09-09', 1, 'Large Bag', 'cntr2', 'cntr5', 'bob@123.ca', 2),
        (30, 10, '2018-09-10', 1, 'Large Bag', 'cntr2', 'sth1', 'bob@123.ca', 2),
        (31, 10, '2018-09-11', 1, 'Large Bag', 'cntr2', 'sth2', 'bob@123.ca', 2),
        (32, 10, '2018-09-12', 1, 'Large Bag', 'cntr2', 'sth3', 'bob@123.ca', 2),
        (33, 10, '2018-09-01', 1, 'Large Bag', 'cntr2', 'cntr1', 'don@mayor.yeg', 3),
        (34, 10, '2018-09-02', 1, 'Large Bag', 'cntr2', 'nrth1', 'don@mayor.yeg', 3),
        (35, 10, '2018-09-03', 1, 'Large Bag', 'cntr2', 'cntr3', 'don@mayor.yeg', 3),
        (36, 10, '2018-09-04', 1, 'Large Bag', 'cntr2', 'cntr4', 'don@mayor.yeg', 3),
        (37, 10, '2018-09-05', 1, 'Large Bag', 'cntr2', 'sth1', 'don@mayor.yeg', 3),
        (38, 10, '2018-09-06', 1, 'Large Bag', 'cntr2', 'sth2', 'don@mayor.yeg', 3),
        (39, 10, '2018-09-07', 1, 'Large Bag', 'cntr2', 'sth3', 'don@mayor.yeg', 3),
        (40, 50, '2018-09-08', 1, 'Large Bag', 'cntr2', 'yyc1', 'don@mayor.yeg', 3),
        (41, 100, '2018-11-05', 2, 'Large Bag', 'cntr1', 'sk1', 'don@mayor.yeg', 3),
        (42, 150, '2018-11-05', 2, 'Large Bag', 'van2', 'nrth2', 'don@mayor.yeg', 3),
        (43, 10, '2018-10-14', 4, 'Large Bag', 'sth4', 'yyc1', 'jane_doe@abc.ca', 1);

-- |bno|email|rno|cost|seats|pickup|dropoff|
insert into bookings values
        (1, 'connor@oil.com', 1, null, 1, null, null),
        (2, 'connor@oil.com', 2, null, 1, null, null),
        (3, 'kd@lang.ca', 3, 45, 1, 'cntr2', null),
        (4, 'reilly@esks.org', 4, 30, 13, null, null),
        (5, 'don@mayor.yeg', 5, 50, 1, 'cntr2', 'yyc3'),
        (6, 'marty@mc.fly', 18, null, 3, null, null),
        (7, 'darryl@oil.com', 20, null, 1, null, null),
        (8, 'john@acorn.nut', 26, null, 1, null, null),
        (9, 'cadence@rap.fm', 27, null, 1, null, null),
        (10, 'connor@oil.com', 5, 45, 1, null, null),
        (11, 'mal@serenity.ca', 41, null, 1, null, null),
        (12, 'nellie@five.gov', 42, null, 1, null, null);

-- |rno|lcode|
insert into enroute values
        (12, 'yyc1'),
        (16, 'sk1'),
        (17, 'cntr2');
        
-- |rid|email|rdate|pickup|dropoff|amount|
insert into requests values
        (1, 'darryl@oil.com', '2018-07-23', 'nrth1', 'cntr1', 10),
        (2, 'nellie@five.gov', '2018-07-22', 'west1', 'sth4', 10),
        (3, 'mal@serenity.ca', '2018-10-11', 'nrth2', 'sth3', 10),
        (4, 'don@mayor.yeg', '2018-10-11', 'nrth2', 'sth3', 10),
        (5, 'the99@oil.com', '2018-10-11', 'nrth1', 'ab1', 10),
        (6, 'marty@mc.fly', '2018-10-11', 'sk1', 'sth3', 10),
        (7, 'mess@marky.mark', '2018-10-11', 'nrth2', 'sth3', 1),
        (8, 'mess@marky.mark', '2018-10-11', 'nrth2', 'sth3', 100),
        (9, 'jane_doe@abc.ca', '2018-04-26', 'cntr3', 'cntr2', 10);

-- |email|msgTimestamp|sender|content|rno|seen|
insert into inbox values
        ('don@mayor.yeg', '2018-08-04', 'darryl@oil.com', 'message content is here', 36, 'n'),
        ('jane_doe@abc.ca', '2018-09-04', 'darryl@oil.com', '2nd message content is here', 43, 'n'),
        ('don@mayor.yeg', '2018-10-04', 'darryl@oil.com', '3rd message content is here', 42, 'n');
                        '''

    cursor.executescript(insert_query)
    
    connection.commit()
    return


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
        and pwd = '{1}' COLLATE NOCASE; '''.format(user, password))
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
    define_tables()
    insert_data()
    member = sign_in_screen()
    while True:
        member = operations(member)
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
