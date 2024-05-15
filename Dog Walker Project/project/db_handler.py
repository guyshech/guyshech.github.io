import MySQLdb
#define the connection data
DB_USER_NAME='team19'
DB_PASSWORD='vszpdnjr'
DB_DEFALUT_DB='team19'
class DbHandler():
    def __init__(self):
        #define the connection to DB information
        self.m_user = DB_USER_NAME
        self.m_password = DB_PASSWORD
        self.m_default_db = DB_DEFALUT_DB
        self.m_charset ='utf8'
        self.m_host = '34.135.7.76'
        self.m_port = 3306
        self.m_DbConnection = None
#connecting to the DB with the information defined
    def connectToDb(self):
        if self.m_DbConnection is None: self.m_DbConnection = MySQLdb.connect(host=self.m_host, db=self.m_default_db,
                                                                              port=self.m_port, user=self.m_user,
                                                                              passwd=self.m_password, charset=self.m_charset)
#commiting function
    def commit(self):
        if self.m_DbConnection: self.m_DbConnection.commit()
#disconnection from DB function
    def disconnectFromDb(self):
        if self.m_DbConnection:
            self.m_DbConnection.close()
            self.m_DbConnection = None
#cursor function
    def getCursor(self):
        #connectin and do the cursor
        self.connectToDb()
        return (self.m_DbConnection.cursor())
