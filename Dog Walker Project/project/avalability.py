# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
# import the class User
from user import User
# import the class service_provider
from service_provider import service_provider
#define a new class of the avalability of a servise provider
class avalability(service_provider):
    def __init__(self):
        logging.info('Initializing Avalability')
        self.a_DbHandler=db_handler.DbHandler()
        # create data members of the class Message and initializing a day and a part of day
        service_provider.__init__(self)
        self.a_day = ""
        self.a_part_of_day = ""
#define a function that will insert to the database the avalability of servise provider
    def insertToDb(self):
        # First, we check if the walker already exists as a User
        self.u_DbHandler = db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        cursor.execute('SELECT Email FROM User where Email="' + self.u_email + '"')
        checker = cursor.fetchall()
        #is the walker is not exists 
        if not checker:
            # Inserting the values of object walker to the DB
            User.insertToDb(self)
        # Inserting the object of servise provider to the DB
        self.a_DbHandler.connectToDb()
        cursor = self.a_DbHandler.getCursor()
        sql = """INSERT INTO Service_Provider(Av_Day, Av_Part_Of_Day, Email) VALUES(%s,%s,%s)"""
        cursor.execute(sql, (self.a_day, self.a_part_of_day,self.u_email))
        self.a_DbHandler.commit()
        #disconnecting from the data base
        self.a_DbHandler.disconnectFromDb()
        return
