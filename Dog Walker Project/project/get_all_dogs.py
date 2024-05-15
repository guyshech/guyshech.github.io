import db_handler

# Function to get all the dogs of this owner - prevents duplicated code
def get_all_dogs(user):
    # Creates db_handler object - to connect to the DB
    d_DbHandler = db_handler.DbHandler()
    cursor = d_DbHandler.getCursor()
    # Getting all the dogs and their features
    cursor.execute('SELECT * FROM Dog WHERE Email="' + user.email() + '"')
    dogs = []
    temps = cursor.fetchall()
    #adding to the list of dogs each dog that the owner have in th DB
    for temp in temps:
        temp_dict = {}
        temp_dict['ID'] = str(temp[0])
        temp_dict['Name'] = str(temp[6])
        temp_dict['Sex'] = str(temp[3])
        temp_dict['Weight'] = str(temp[5])
        temp_dict['Age'] = str(temp[4])
        temp_dict['Trained'] = temp[1]
        temp_dict['Vaccinated'] = temp[2]
        temp_dict['Email'] = str(temp[7])
        dogs.append(temp_dict)
    #disconnecting from the DB
    d_DbHandler.disconnectFromDb()
    return dogs
