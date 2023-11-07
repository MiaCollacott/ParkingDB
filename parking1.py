import sqlite3
"""Notice I have set up an intial structure and then started to ..  think about the things I want to
automate for my users later. (By 'started to ..' I of course mean, left for you to do!!!)
By defining these as methods on a DB class I can reuse them easily,
In particular I can separate this section out later on, then import it, with the methods as
a module in other files."""
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("parking1.db", detect_types=sqlite3.PARSE_DECLTYPES |
                                    sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")
        self.conn.commit()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tbl_customers
    (customer_id INTEGER PRIMARY KEY,
     surname TEXT NOT NULL,
     forename TEXT NOT NULL,
     disabled INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0,
     type TEXT NOT NULL CHECK (type = "Staff" OR type = "Student"),
     current INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 1)
                """)
        self.conn.commit()
        
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tbl_cars
    (reg TEXT PRIMARY KEY,
    make TEXT NOT NULL,
    model TEXT NOT NULL)""")
        self.conn.commit()
        
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tbl_terms
    (term TEXT PRIMARY KEY,
    staff_price REAL NOT NULL,
    student_price REAL NOT NULL,
    disabled_price REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0)
    """)
        self.conn.commit()
        
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tbl_spaces
    (space TEXT PRIMARY KEY,    
    disabled INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 0)
    """)        
        self.conn.commit()
        
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tbl_sales
    (sold_term TEXT NOT NULL,
    sold_space TEXT NOT NULL,
    customer_id INTEGER NOT NULL,
    price_paid REAL NOT NULL ON CONFLICT REPLACE DEFAULT 0,
    PRIMARY KEY (sold_term, sold_space),
    FOREIGN KEY (sold_term) REFERENCES tbl_terms(term),
    FOREIGN KEY (sold_space) REFERENCES tbl_spaces(space),    
    FOREIGN KEY (customer_id) REFERENCES tbl_customers(customer_id)    
    )
    """)        
        self.conn.commit()       

        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS tbl_owners
    (car_owner INTEGER NOT NULL,
    car_reg TEXT NOT NULL,
    current_car INTEGER NOT NULL ON CONFLICT REPLACE DEFAULT 1,
    PRIMARY KEY (car_owner, car_reg),
    FOREIGN KEY (car_owner) REFERENCES tbl_customers(customer_id),
    FOREIGN KEY (car_reg) REFERENCES tbl_cars(reg)    
    )
    """)        
        self.conn.commit() 
        
        self.conn.close()
    def openDb(self):
        self.conn = sqlite3.connect("parking1.db")
        self.cur = self.conn.cursor()
    def closeDb(self):
        self.conn.close()       
    def viewCustomers(self):
        self.cur.execute("SELECT * FROM tbl_customers")
        rows = self.cur.fetchall()
        return rows
    def insertCustomer(self, rqsurname  , rqforename, rqdisability, rqtype ):
        self.cur.execute("INSERT INTO tbl_customers (surname, forename, disabled, type) VALUES (?,?,?,?)",
                         (rqsurname  , rqforename, rqdisability, rqtype))
        self.conn.commit()
        
    def insertCar(self, rqreg, rqmake, rqmodel):
        self.cur.execute("INSERT INTO tbl_cars (reg, make, model) VALUES (?,?,?)",(rqreg, rqmake, rqmodel))
        self.conn.commit()
    def viewCarsall(self):
        self.cur.execute("SELECT * FROM tbl_cars")
        rows = self.cur.fetchall()
        return rows
    def viewCarsCurrent(self):
        self.cur.execute("SELECT * FROM tbl_owners WHERE current = 1")
        rows = self.cur.fetchall()
        return rows       
    def viewCarsNotcurrent(self):
        self.cur.execute("SELECT * FROM tbl_owners WHERE available = 0")
        rows = self.cur.fetchall()
        return rows
#Why would this be a bad idea?? (Consider data integrity!!)   
    def removeCar(self, rqreg):
        self.cur.execute("DELETE * FROM tbl_cars WHERE reg = ?",(rqreg,))
        self.conn.commit()
#add owner
    def addOwner(self, rqreg):
        self.cur.execute("INSERT INTO tbl_owners (car_owner, car_reg, current_car) VALUES (?,?,?)")
        self.conn.commit()
#Removing a car? Best to mark it as not currently owned!
    def mark_Notcurrent(self, rqreg):
        self.cur.execute("UPDATE tbl_owners SET current = 0 WHERE reg = ? AND current = 1",(rqreg,))
        self.conn.commit()
#enter user and sell space
    def customerInput(self):
        forenameinput = input("What is your first name? ")
        surnameinput = input("What is your surname? ")
        disabledinput = input("Are you disabled? (Y/N) ")
        if disabledinput == 'Y':
            disabledinput = 1
        else:
            disabledinput = 0
        typeinput = input("Staff or Student?")
        mydatabase.insertCustomer(surnameinput, forenameinput, disabledinput, typeinput )
        self.conn.commit()
        
    def carInput(self):    
        reginput = input ("Car reg: ")
        makeinput = input ("Input make: ")
        modelinput = input("Input model: ")
        mydatabase.insertCar(reginput, makeinput, modelinput)
        self.conn.commit()
#link car to user
    def carLink(self):
        idinput = input("Enter customer ID: ")
        reginput = input ("Car reg: ")
        currentinput = input ("Is the car current? (Y/N) ")
        if currentinput == "Y":
            currentinput = 1
        else:
            currentinput = 0
        addOwner(idinput, reginput, currentinput)
        self.conn.commit()
# Reversing this could be tricky, why?
#Is there a case for having a currently_owned flag in the cars table?




#Use the class to create a database and use the .openDb() and .clseDb() methods
mydatabase = DB()
mydatabase.openDb()
customers = mydatabase.viewCustomers()
owners = mydatabase.viewCarsall()
mydatabase.customerInput()
mydatabase.carInput()
mydatabase.carLink()
print(customers)
print (owners)
mydatabase.closeDb()

""" Consider the required functionality of the database.  What other methods can you
put in place to automate the use of the database? """

#Use your methods to add some test data to the database.


