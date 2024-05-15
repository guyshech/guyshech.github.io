# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
from user import User
#define a new class for a dog owner
class dog_owner(User):
    def __init__(self):
        logging.info('Initializing Dog_Owner')
        self.do_DbHandler=db_handler.DbHandler()
        # create data members of the class Message
        User.__init__(self)
        self.do_birthdate = ""
#function which insert the information given for a dog owner
    def insertToDb(self):
        # First, we check if the walker already exists as a User
        self.u_DbHandler = db_handler.DbHandler()
        cursor = self.u_DbHandler.getCursor()
        #check is the user email is in the DB
        cursor.execute('SELECT Email FROM User where Email="' + self.u_email + '"')
        checker = cursor.fetchall()
        if not checker:
            # Inserting the values of object owner to the DB
            User.insertToDb(self)
        # Inserting the object of owner to the DB
        self.do_DbHandler.connectToDb()
        cursor = self.do_DbHandler.getCursor()
        sql = """INSERT INTO Dog_Owner(Birth_Date, Email) VALUES(%s,%s)"""
        cursor.execute(sql, (self.do_birthdate, self.u_email))
        self.do_DbHandler.commit()
        #disconnet from the DB
        self.do_DbHandler.disconnectFromDb()
        return
