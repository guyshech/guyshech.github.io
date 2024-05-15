# import logging so we can write messages to the log
import logging
# import the class DbHandler to interact with the database
import db_handler
#define a new class for a user
class User():
    def __init__(self):
        logging.info('Initializing User')
        self.u_DbHandler=db_handler.DbHandler()
        # create data members of the class Message
        self.u_email = ""
        self.u_city = ""
        self.u_phone= ""
        self.u_name = ""

        
   # insert a new user to the database
    def insertToDb(self):
        self.u_DbHandler.connectToDb()
        cursor = self.u_DbHandler.getCursor()
        sql = """INSERT INTO User(Email,Phone,Name,City)
        VALUES(%s,%s,%s,%s)
        """
        cursor.execute(sql,
                       (self.u_email, self.u_phone, self.u_name, self.u_city))
        self.u_DbHandler.commit()
        #disconnecting from the DB
        self.u_DbHandler.disconnectFromDb()
        return


