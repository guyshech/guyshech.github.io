# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
from user import User
from service_provider import service_provider
#define a new class for dog walker

class dog_walker(service_provider):
    def __init__(self):
        logging.info('Initializing Dog_Walker')
        self.dw_DbHandler=db_handler.DbHandler()
        # create data members of the class dog walker
        service_provider.__init__(self)
        self.dw_max_dogs = ""
        self.dw_seniority = ""
        self.dw_small = ""
        self.dw_medium = ""
        self.dw_large = ""
        self.dw_vaccine = ""
        self.dw_trained = ""
#define a function which insert the information to the DB
    def insertToDb(self):
        # First, we check if the walker already exists as a User
        self.u_DbHandler = db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        cursor.execute('SELECT Email FROM User where Email="' + self.u_email + '"')
        checker = cursor.fetchall()
        if not checker:
            # Inserting the values of object walker to the DB
            service_provider.insertToDb(self)
        # Inserting the object of owner to the DB
        self.dw_DbHandler.connectToDb()
        cursor = self.dw_DbHandler.getCursor()
        sql = """INSERT INTO Dog_Walker(Max_Dogs, Seniority, S, M, L, Vaccine_Res, Trained_Res, Email)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.dw_max_dogs, self.dw_seniority, self.dw_small, self.dw_medium, self.dw_large, self.dw_vaccine,self.dw_trained ,self.u_email))
        self.dw_DbHandler.commit()
        #disconnet from the DB
        self.dw_DbHandler.disconnectFromDb()
        return
