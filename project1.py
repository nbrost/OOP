import sqlite3
import time

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def drop_tables():
    global connection, cursor

    drop_course = "DROP TABLE IF EXISTS course; "
    drop_student = "DROP TABLE IF EXISTS student; "
    drop_enroll = "DROP TABLE IF EXISTS enroll; "

    drop_requests = "drop table if exists requests;"
    drop_enroute = "drop table if exists enroute;"
    drop_bookings = "drop table if exists bookings;"
    drop_rides = "drop table if exists rides; "
    drop_locations = "drop table if exists locations;"
    drop_cars = "drop table if exists cars;"
    drop_members = "drop table if exists members;"
    drop_inbox = "drop table if exists inbox;"


    cursor.execute(drop_enroll)
    cursor.execute(drop_student)
    cursor.execute(drop_course)
    cursor.execute(drop_requests)
    cursor.execute(drop_enroute)
    cursor.execute(drop_bookings)
    cursor.execute(drop_rides)
    cursor.execute(drop_locations)
    cursor.execute(drop_cars)
    cursor.execute(drop_members)
    cursor.execute(drop_inbox)


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


def insert_data():
    global connection, cursor

    insert_courses = '''
                        INSERT INTO course(course_id, title, seats_available) VALUES
                            (1, 'CMPUT 291', 200),
                            (2, 'CMPUT 391', 100),
                            (3, 'CMPUT 101', 300);
                    '''

    insert_students = '''
                            INSERT INTO student(student_id, name) VALUES
                                    (1509106, 'Jeff'),
                                    (1409106, 'Alex'),
                                    (1609106, 'Mike');
                            '''

    cursor.execute(insert_courses)
    cursor.execute(insert_students)
    connection.commit()
    return


def enroll(student_id, course_id):
    global connection, cursor

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    """
    	Check that there is a spot in the course for this student.
    """

    """ 
        Register the student in the course.
    """

    """
    	Update the seats_available in the course table. (decrement)
    """

    connection.commit()
    return

def sign_in():
    global connection, cursor
    while True:
        user = input("Enter email or quit: ")
        if user == "quit":
            return None
        password = input("Enter Password: ")
        log_in_query = ('''
        select email, name, phone, pwd
        from members
        where email = '{0}'
        and pwd = '{1}'; '''.format(user, password))
        cursor.execute(log_in_query)
        member = cursor.fetchall()
        
        if member == []:
            return None
        return member[0]
        


def main():
    global connection, cursor

    path = "./rideshare.db"
    connect(path)
    #drop_tables()
    #define_tables()
    #insert_data()
    sign_in_flag = int(input("Press 1 to sign in or 2 to create a new user: "))
    if sign_in_flag == 1:
        member = sign_in()
    print (member)
    #else:
    #    create_user()
    
    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
