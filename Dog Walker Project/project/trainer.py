# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
from user import User
from service_provider import service_provider
#define a new class for a trainer 
class trainer(service_provider):
    def __init__(self):
        logging.info('Initializing Trainer')
        self.t_DbHandler=db_handler.DbHandler()
        # create data members of the class trainer
        service_provider.__init__(self)
        self.t_institute = ""
        self.t_num_dogs = ""
        self.t_graduation_date = ""
        self.t_training_types = ""
        self.t_price = ""
#define a function that will insert the information of a trainer to the DB
    def insertToDb(self):
        # First, we check if the walker already exists as a User
        self.u_DbHandler = db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        cursor.execute('SELECT Email FROM User where Email="' + self.u_email + '"')
        checker = cursor.fetchall()
        if not checker:
            # Inserting the values of object owner to the DB
            service_provider.insertToDb(self)
        # Inserting the object of trainer to the DB
        self.t_DbHandler.connectToDb()
        cursor = self.t_DbHandler.getCursor()
        sql = """INSERT INTO Trainer(Institute_Of_Study, Num_Of_Trained_Dogs, Graduation_Date, Training_Types, Trainer_Price, Email)  VALUES(%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.t_institute, self.t_num_dogs, self.t_graduation_date, self.t_training_types, self.t_price ,self.u_email))
        self.t_DbHandler.commit()
        #disconnecting from the DB
        self.t_DbHandler.disconnectFromDb()
        return
