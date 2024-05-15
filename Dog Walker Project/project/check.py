import db_handler
# Functions to check if the user exist in db in three ways: as Dog Owner or as Dog Walker or as Trainer.


def check_if_owner(email):
    # Using db_handler - to connect to the DB
    u_DbHandler=db_handler.DbHandler()
    cursor = u_DbHandler.getCursor()
    #execute and check if the email is on the dog owner table in the DB
    cursor.execute('SELECT Email FROM Dog_Owner WHERE Email="'+email+'"')
    check_owner = cursor.fetchall()
    if check_owner:
        return True
    return False

def check_if_walker(email):
    # Using db_handler - to connect to the DB
    u_DbHandler=db_handler.DbHandler()
    cursor = u_DbHandler.getCursor()
    #execute and check if the email is on the dog walker table in the DB
    cursor.execute('SELECT Email FROM Dog_Walker WHERE Email="'+email+'"')
    check_walker = cursor.fetchall()
    if check_walker:
        return True
    return False

def check_if_trainer(email):
    # Using db_handler - to connect to the DB
    u_DbHandler=db_handler.DbHandler()
    cursor = u_DbHandler.getCursor()
    #execute and check if the email is on the dog trainer table in the DB
    cursor.execute('SELECT Email FROM Trainer WHERE Email="'+email+'"')
    check_trainer = cursor.fetchall()
    if check_trainer:
        return True
    return False
