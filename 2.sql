-- Data originally prepared by Tanner Chell, tchell@ualberta.ca,
-- published on 2018-Oct-05
-- modified by Nicholas Leong, nleong1@ualberta.ca for miniProject 1

-- |email|name|phone|pwd|
insert into members values 
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
