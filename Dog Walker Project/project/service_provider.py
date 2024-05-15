# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
from user import User
#define a new ckass for servise provider
class service_provider(User):
    def __init__(self):
        logging.info('Initializing Service_Provider')
        self.sp_DbHandler=db_handler.DbHandler()
        # create data members of the class servise provider
        User.__init__(self)
        self.sp_street = ""
        self.sp_house_number = ""
        self.sp_availability = {'Sunday': {'Morning': False, 'Noon': False, 'Evening': False},
                             'Monday': {'Morning': False, 'Noon': False, 'Evening': False},
                             'Tuesday': {'Morning': False, 'Noon': False, 'Evening': False},
                             'Wednesday': {'Morning': False, 'Noon': False, 'Evening': False},
                             'Thursday': {'Morning': False, 'Noon': False, 'Evening': False},
                             'Friday': {'Morning': False, 'Noon': False, 'Evening': False},
                             'Saturday': {'Morning': False, 'Noon': False, 'Evening': False}}
#define a function that will insert the information of a servise provider to the DB
    def insertToDb(self):
        # First, we check if the walker already exists as a User
        self.u_DbHandler = db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        #check if the email given is in the DB
        cursor.execute('SELECT Email FROM User where Email="' + self.u_email + '"')
        checker = cursor.fetchall()
        if not checker:
            # Inserting the values of object user to the DB
            User.insertToDb(self)
        # Inserting the object of servise provider to the DB
        self.sp_DbHandler.connectToDb()
        cursor = self.sp_DbHandler.getCursor()
        sql = """INSERT INTO Service_Provider(Street, House_Number, Email) VALUES(%s,%s,%s)"""
        cursor.execute(sql, (self.sp_street, self.sp_house_number,self.u_email))
        self.sp_DbHandler.commit()
        # Inserting the days and parts in days that the walker is able to walk
        cursor2 = self.sp_DbHandler.getCursor()
        for day in self.sp_availability:
            for part in self.sp_availability[day]:
                if self.sp_availability[day][part]:
                    sql = """INSERT INTO Avalability(Email, Av_Day ,Av_Part_Of_Day) VALUES(%s,%s,%s)"""
                    cursor2.execute(sql, (self.u_email, day, part))
        self.sp_DbHandler.commit()
        #disconnecting from DB
        self.sp_DbHandler.disconnectFromDb()
        return
