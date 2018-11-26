from bsddb3 import db
DB_File = "pr.idx"

database = db.DB()
database.open(DB_File,None, db.DB_BTREE, db.DB_RDONLY)
curs = database.cursor()
iter = curs.first()
while (iter):
    print(curs.count()) #prints no. of rows that have the same key for the current key-value pair referred by the cursor
    print(iter)

    #iterating through duplicates
    dup = curs.next_dup()
    while(dup!=None):
        print(dup)
        dup = curs.next_dup()

    iter = curs.next()

curs.close()
database.close()