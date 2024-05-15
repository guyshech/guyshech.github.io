# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#define a new class for a dog
class dog():

    def __init__(self):
        logging.info('Initializing Dog')
        self.d_DbHandler=db_handler.DbHandler()
        # Creates data members of the class Dog
        self.d_id = ""
        self.d_trained = False
        self.d_vaccinated = False
        self.d_sex = ""
        self.d_age = ""
        self.d_weight = ""
        self.d_name = ""
        self.dog_owner_email = ""
#define a function which insert the information of a dog to the DB
    def insertToDb(self):
        # Inserting the object of dog to the DB
        self.d_DbHandler.connectToDb()
        cursor = self.d_DbHandler.getCursor()
        sql = """INSERT INTO Dog(ID, Trained, Vaccinated,Sex, Age, Weight, Name, Email ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (self.d_id, self.d_trained, self.d_vaccinated, self.d_sex, self.d_age, self.d_weight, self.d_name, self.dog_owner_email))
        self.d_DbHandler.commit()
        #disconnecting from the DB
        self.d_DbHandler.disconnectFromDb()
        return
