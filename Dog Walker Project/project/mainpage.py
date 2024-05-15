# Import webapp2  - Python web framework compatible with Google App Engine
import webapp2
# Import Jinja and os libraries
import jinja2
import os
# Import logging so we can write in the console
import logging
# Import users library - To login with google account
from google.appengine.api import users
# Import all objects of our DB
import db_handler
import user
import service_provider
import request
import dog_owner
import trainer
import dog_walker
import review
import avalability
import dog
# Import checks that preformed on the input
from check import check_if_owner, check_if_walker, check_if_trainer
# Import get all dog function that returns al the dogs that belong to a specific owner
from get_all_dogs import get_all_dogs
# Import date library
from datetime import date
# define variables that we will use in the classes
d_id_req_w = None
d_days_req_w = None
d_part_of_days_req_w = None
d_id_req_t = None
d_days_req_t = None
d_part_of_days_req_t = None
# Load Jinja
jinja_environment = jinja2.Environment(loader=
                                      jinja2.FileSystemLoader
                                     (os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
        def get(self):
            # Create a template object
            main_page_template = jinja_environment.get_template('first_login.html')
            user = users.get_current_user()
            # if is logged in
            if user:
                # get the nickname from the user object
                nickname = user.nickname()
                logging.info('nickname is ' + nickname)
                # checking the user affiliation(Owner, Trainer or Walker)
                if check_if_owner(user.email()):
                    self.redirect('/homepage_dog_owner')
                elif check_if_walker(user.email()):
                    self.redirect('/homepage_worker')
                elif check_if_trainer(user.email()):
                    self.redirect('/homepage_worker')
                else:
                    self.redirect('/sign_up')
            # Creating an HTML page and response
            self.response.write(main_page_template.render())

# -----------------------------------------
# class to login to the google account
# redirect to sign up page or home page accordingly
# -----------------------------------------

class Login(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # If the user object exists (the user is logged in to google)
        if user:
            # checking the user affiliation(owner, trainer or dog-walker)
            if check_if_owner(user.email()):
                self.redirect('/homepage_dog_owner')
            if check_if_walker(user.email()):
                self.redirect('/homepage_worker')
            if check_if_trainer(user.email()):
                self.redirect('/homepage_worker')
        # If the user object does not exist we will transfer him to registration page
        else:
            self.redirect(users.create_login_url('/sign_up'))
# -----------------------------------------
# class to logout from the google account
# and show main page again
# Handles /logout
# -----------------------------------------

class Logout(webapp2.RequestHandler):
    def get(self):
        # if the user is logged in - we will perform log out
        user = users.get_current_user()
        if user:
            logging.info('The user is logged in - performing logout ')
            # force the user to logout and redirect him afterward to
            # Main page
            self.redirect(users.create_logout_url('/'))

        else:
            self.redirect('/')



# ---------------------------------------------------------
# First Login - Here a new user selects whether he is a Dog Owner
# or a Dog Walker or a Trainer
# Handles /first_login
# --------------------------------------------------------
class FirstLogin(webapp2.RequestHandler):
    def get(self):
        # Create a template object
        first_login_template = jinja_environment.get_template('sign_up.html')
        user = users.get_current_user()
        # If the user already exist in our DB (Owner, Trainer or Walker), he redirects to his homepage
        if user:
            # logging.info('The user object exists????')
            if check_if_owner(user.email()):
                self.redirect('/homepage_dog_owner')
            elif check_if_walker(user.email()):
                self.redirect('/homepage_worker')
            elif check_if_trainer(user.email()):
                self.redirect('/homepage_worker')

        # Else, he needs to choose if he is a walker or owner
        # Creating an HTML page and response
        self.response.write(first_login_template.render())

# -----------------------------------------
# class to register a new dog owner
# -----------------------------------------

class DogOwnerRegister(webapp2.RequestHandler):
    # There is a 'get' function to get the form and show it, and a 'post' function to handle what we get from it
    def get(self):
        # Create a template object
        first_login_template = jinja_environment.get_template('register_dog_owner.html')
        # Creating an HTML page and response
        self.response.write(first_login_template.render())

    def post(self):
        # Retrieve data from the POST request
        user1 = users.get_current_user()
        if not check_if_owner(user1.email()):
            # Using class Dog_Owner - to insert to DB
            owner = dog_owner.dog_owner()
            owner.u_email = user1.email()
            owner.u_name = str(self.request.get('name'))
            owner.do_birthdate = self.request.get('birthday')
            owner.u_phone = str(self.request.get('phone'))
            owner.u_city = str(self.request.get('city')).replace("-", " ").lower()
            owner.insertToDb()
        # Redirects to the Dog Owner homepage
        self.redirect('/homepage_dog_owner')


# ---------------------------------------------------------
# Add a new dog for Dog Owner
# --------------------------------------------------------
class AddNewDog(webapp2.RequestHandler):

    # There is a 'get' function to get the form and show it, and a 'post' function to handle what we get from it.
    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('register_dog.html')
        # Creating an HTML page and response
        self.response.write(first_login_template.render())

    def post(self):
        # Retrieve data from the POST request
        user = users.get_current_user()
        # Using class Dog - to insert to DB
        dog1 = dog.dog()
        dog1.d_id = int(self.request.get('id'))
        dog1.d_name = str(self.request.get('name'))
        dog1.d_sex = str(self.request.get('sex'))
        dog1.d_weight = int(self.request.get('weight'))
        dog1.d_age = int(self.request.get('age'))
        dog1.d_trained = str(self.request.get('Trained'))
        dog1.d_vaccinated = str(self.request.get('Vaccinated'))
        dog1.dog_owner_email = user.email()
        # According to the dog's weight we will keep its size
        if (dog1.d_weight<=10):
            dog1.d_weight = 'Small'
        if ((dog1.d_weight>10)and(dog1.d_weight<=20)):
            dog1.d_weight = 'Medium'
        else:
            dog1.d_weight = 'Large'
        dog1.insertToDb()
        # Redirects to the Dog Owner homepage
        self.redirect('/homepage_dog_owner')


# ---------------------------------------------------------
# Dog Walker Register - Here a new Dog Walker fills out his/her details
# --------------------------------------------------------

class DogWalkerRegister(webapp2.RequestHandler):
    # There is a 'get' function to get the form and show it, and a 'post' function to handle what we get from it.
    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('register_dog_walker.html')
        # Creating an HTML page and response
        # Creating a dictionary on which we will run in the html page
        parameters_for_template = {'days':['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'parts_of_day':['Morning','Noon','Evening']}
        self.response.write(first_login_template.render(parameters_for_template))

    def post(self):

        user = users.get_current_user()
        # Using the Dog_Walker class - to insert to DB
        walker = dog_walker.dog_walker()
        walker.u_email = user.email()
        walker.u_name = str(self.request.get('name'))
        walker.u_city = str(self.request.get('city')).replace("-", " ").lower()
        walker.u_phone = str(self.request.get('phone'))
        walker.sp_street = str(self.request.get('street'))
        walker.sp_house_number = int(self.request.get('house_number'))
        walker.dw_max_dogs = int(self.request.get('max_dogs'))
        walker.dw_seniority = int(self.request.get('seniority'))
        walker.dw_small = int(self.request.get('small_price'))
        walker.dw_medium = int(self.request.get('med_price'))
        walker.dw_large = int(self.request.get('big_price'))
        walker.dw_vaccine = str(self.request.get('Restrictions1'))
        walker.dw_trained = str(self.request.get('Restrictions2'))
        dict_temp_days_and_parts = {'Sunday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Monday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Tuesday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Wednesday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Thursday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Friday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Saturday': {'Morning': False, 'Noon': False, 'Evening': False}}
        for day in dict_temp_days_and_parts:
            for part in dict_temp_days_and_parts[day]:
                temp_str = day+'-'+part
                temp = self.request.get(temp_str)
                if temp == temp_str:
                    dict_temp_days_and_parts[day][part] = True
                else:
                    dict_temp_days_and_parts[day][part] = False
        walker.sp_availability = dict_temp_days_and_parts
        walker.insertToDb()
        # Redirects back to Worker homepage
        self.redirect('/homepage_worker')

# ---------------------------------------------------------
# Trainer Register - Here a new trainer fills out his/her details
# --------------------------------------------------------

class TrainerRegister(webapp2.RequestHandler):
    # There is a 'get' function to get the form and show it, and a 'post' function to handle what we get from it.
    def get(self):

        # Create a template object
        first_login_template = jinja_environment.get_template('register_trainer.html')
        # Creating an HTML page and response
        parameters_for_template = {
            'days': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'parts_of_day': ['Morning', 'Noon', 'Evening']
        }
        self.response.write(first_login_template.render(parameters_for_template))

    def post(self):

        user = users.get_current_user()
        # Using the Dog_Walker class - to insert to DB
        dog_trainer = trainer.trainer()
        dog_trainer.u_email = user.email()
        dog_trainer.u_name = self.request.get('name')
        dog_trainer.u_city = self.request.get('city').replace("-", " ").lower()
        dog_trainer.u_phone = self.request.get('phone')
        dog_trainer.sp_street = self.request.get('street')
        dog_trainer.sp_house_number = self.request.get('house_number')
        dog_trainer.t_institute = self.request.get('Graduation_College')
        dog_trainer.t_num_dogs = self.request.get('num_of_dogs')
        dog_trainer.t_graduation_date = self.request.get('Graduation_Date')
        dog_trainer.t_training_types = self.request.get('Type_Of_Training')
        dog_trainer.t_price = self.request.get('price')
        dict_temp_days_and_parts = {'Sunday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Monday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Tuesday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Wednesday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Thursday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Friday': {'Morning': False, 'Noon': False, 'Evening': False},
                                    'Saturday': {'Morning': False, 'Noon': False, 'Evening': False}}
        for day in dict_temp_days_and_parts:
            for part in dict_temp_days_and_parts[day]:
                temp_str = day+'-'+part
                temp = self.request.get(temp_str)
                if temp == temp_str:
                    dict_temp_days_and_parts[day][part] = True
                else:
                    dict_temp_days_and_parts[day][part] = False
        dog_trainer.sp_availability = dict_temp_days_and_parts
        dog_trainer.insertToDb()
        # Redirects back to Worker homepage
        self.redirect('/homepage_worker')


# ---------------------------------------------------------
# Set a new walk - first layer filter
# --------------------------------------------------------

class WalkRequest(webapp2.RequestHandler):
    def get(self):
        # Create a template object
        walk_request_template = jinja_environment.get_template('walk_request.html')
        user = users.get_current_user()
        # sets dogs to a list that consists all the dogs that belongs to the owner
        dogs = get_all_dogs(user)
        # Getting the day and part of day for the walk
        parameters_for_template = {
            'days': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'parts_of_day': ['Morning', 'Noon', 'Evening'],
            'dogs': dogs,
        }
        self.response.write(walk_request_template.render(parameters_for_template))

    def post(self):
        # Retrieve data from the POST request
        # saves the data inserted by the dog owner
        global d_id_req_w
        d_id_req_w = str(self.request.get('dogs'))
        global d_days_req_w
        d_days_req_w = str(self.request.get('days'))
        global d_part_of_days_req_w
        d_part_of_days_req_w = str(self.request.get('parts_of_day'))
        # Redirects to relevant walkers
        self.redirect('/relevant_walker')

# ---------------------------------------------------------
# Set a new walk - only relevant walkers available
# --------------------------------------------------------

class RelevantWalker(webapp2.RequestHandler):
    def get(self):
        relevant_walker_template = jinja_environment.get_template('relevant_walker.html')
        global d_id_req_w
        global d_days_req_w
        global d_part_of_days_req_w
        user = users.get_current_user()
        dogs = get_all_dogs(user)
        dog_id = d_id_req_w
        # Creating a list of all the walkers that available on this day, part of day and city of residence
        walkers = []
        # Checks the dog size, vaccination and training status
        for dog in dogs:
            if str(dog['ID']) == dog_id:
                size = str(dog['Weight'])
                vaccinated = dog['Vaccinated']
                trained = dog['Trained']
                break
        day_in_the_week = d_days_req_w
        part_of_day = d_part_of_days_req_w
        # Creates db_handler object - to connect to the DB
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        # Getting from DB the city of residence of the owner so we can get the right walkers
        sql = """SELECT City
                    FROM User
                    WHERE Email = '""" + user.email() + "';"
        cursor.execute(sql)
        city_of_residence_temp = cursor.fetchall()
        # found the owner city
        city_of_residence = str(city_of_residence_temp[0][0])
        # Checking which size so we can get the right price
        costs = {
                "Small": "S",
                "Medium": "M",
                "Large": "L"
            }
        # Checking which walker is not obligated to more dogs than his maximum in the same day and time
        sql = """SELECT Email , COUNT(*)
            FROM Request
             WHERE Av_Day = "%s" and Av_Part_Of_Day="%s" and S_P_Answer='True'
              GROUP BY Email;"""
        sql = sql % (day_in_the_week, part_of_day)
        cursor.execute(sql)
        temps1 = cursor.fetchall()
        # Getting the table of all the walkers that are in the city of residence of the owner and available in the
        # particular day and part of day and are trained/vaccinated according to the service provider's demand
        sql = """SELECT Name, W.Email, Phone, %s, Max_Dogs
                    FROM User AS U JOIN Dog_Walker AS W ON U.Email = W.Email
                        JOIN Avalability As A ON W.Email = A.Email
                    WHERE City = "%s" and Av_Day = "%s" and Av_Part_Of_Day="%s" and ((W.Vaccine_Res <> 'on') or 
                    (W.Vaccine_Res = "%s")) and ((W.Trained_Res  <> 'on') or (W.Trained_Res = "%s")) ;"""
        sql = sql % (costs[size], city_of_residence, day_in_the_week, part_of_day, vaccinated, trained)
        cursor.execute(sql)
        temps = cursor.fetchall()
        # Making a list of all the relevant walkers
        for temp in temps:
            temp_dict = {}
            temp_dict['Name'] = str(temp[0])
            temp_dict['Phone'] = str(temp[2])
            temp_dict['Email'] = str(temp[1])
            temp_dict['Price'] = float(temp[3])
            temp_dict['Max_Dogs'] = int(temp[4])
            walkers.append(temp_dict)
        # removes all the walkers that passes the Max_Dogs limitation
        for t in temps1:
            for walker in walkers:
                if str(t[0]) == walker['Email']:
                    if t[1] >= (walker['Max_Dogs']):
                        walkers.remove(walker)

        parameters_for_template = {
                'walker': walkers
            }
        self.response.write(relevant_walker_template.render(parameters_for_template))

# ---------------------------------------------------------
# Insert the submitted request and redirect to homepage
# --------------------------------------------------------

class InsertRequest(webapp2.RequestHandler):
    def get(self):
        global d_id_req_w
        global d_days_req_w
        global d_part_of_days_req_w
        # Retrieve data from the Get request---->
        # Using class request - to insert to DB---->
        request1 = request.request()
        request1.req_status = "Pending"
        request1.req_dog_id = d_id_req_w
        request1.req_email_service_provider = str(self.request.get('walker_email'))
        request1.req_day = d_days_req_w
        request1.req_part_of_day = d_part_of_days_req_w
        request1.req_creation_time = date.today()
        request1.req_respond_time = date.today()
        request1.insertToDb()
        # Redirects to the Dog Owner homepage
        self.redirect('/homepage_dog_owner')

# ---------------------------------------------------------
# Set a new training - first layer filter
# --------------------------------------------------------

class TrainRequest(webapp2.RequestHandler):

    def get(self):
        # Create a template object
        train_request_template = jinja_environment.get_template('train_request.html')
        user = users.get_current_user()
        # Saves a list of all the owner's dogs using the function get all dogs
        dogs = get_all_dogs(user)
        # Getting the day and part of day for the walk
        parameters_for_template = {
            'days': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'parts_of_day': ['Morning', 'Noon', 'Evening'],
            'dogs': dogs,
        }
        self.response.write(train_request_template.render(parameters_for_template))


    def post(self):
        # Retrieve data from the GET request
        # Using global variables to save the data that inserted by the owner
        global d_id_req_t
        d_id_req_t = str(self.request.get('dogs'))
        global d_days_req_t
        d_days_req_t = str(self.request.get('days'))
        global d_part_of_days_req_t
        d_part_of_days_req_t = str(self.request.get('parts_of_day'))
        # Redirects to relevant trainers page
        self.redirect('/relevant_trainer')

# ---------------------------------------------------------
# Set a new training - only relevant trainers available
# ------------------------------------------------------

class RelevantTrainer(webapp2.RequestHandler):
    def get(self):
        relevant_trainer_template = jinja_environment.get_template('relevant_trainer.html')
        global d_id_req_t
        global d_days_req_t
        global d_part_of_days_req_t
        user = users.get_current_user()
        dogs = get_all_dogs(user)
        dog_id = d_id_req_t
        # Creating a list of all the trainers that available on this day, part of day and city of residence
        trainers = []
        # Checks what is the size, vaccination and training status of the dog
        for dog in dogs:
            if str(dog['ID']) == dog_id:
                size = str(dog['Weight'])
                vaccinated = dog['Vaccinated']
                trained = dog['Trained']
                break
        day_in_the_week = d_days_req_t
        part_of_day = d_part_of_days_req_t
        # Creates db_handler object - to connect to the DB
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        # Getting from DB the city of residence of the owner so we can get the right trainers
        sql = """SELECT City
                    FROM User
                    WHERE Email = '""" + user.email() + "';"
        cursor.execute(sql)
        city_of_residence_temp = cursor.fetchall()
        # found the owner city
        city_of_residence = str(city_of_residence_temp[0][0])
        # Checking which trainer is not obligated to other trainings in the same day and time
        sql = """SELECT Email , COUNT(*)
            FROM Request
             WHERE Av_Day = "%s" and Av_Part_Of_Day="%s" and S_P_Answer='True'
              GROUP BY Email;"""
        sql = sql % (day_in_the_week, part_of_day)
        cursor.execute(sql)
        temps1 = cursor.fetchall()
        # Getting the table of all the trainers that are in the city of residence of the owner and available
        # in the particular day and part of day
        sql = """SELECT Name, T.Email, Phone, Trainer_Price 
                    FROM User AS U JOIN Trainer AS T ON U.Email = T.Email
                        JOIN Avalability As A ON T.Email = A.Email
                    WHERE City = "%s" and Av_Day = "%s" and Av_Part_Of_Day="%s" """
        sql = sql % (city_of_residence, day_in_the_week, part_of_day)
        cursor.execute(sql)
        temps = cursor.fetchall()
        # Making a list of all the relevant trainers
        for temp in temps:
            temp_dict = {}
            temp_dict['Name'] = str(temp[0])
            temp_dict['Phone'] = str(temp[2])
            temp_dict['Email'] = str(temp[1])
            temp_dict['Price'] = float(temp[3])
            trainers.append(temp_dict)
        # removes all the trainers that has a training booked at the same time and day
        for trainer in trainers:
            for temp1 in temps1:
                if str(trainer['Email']) == str(temp1[0]):
                    if int(temp1[1]) == 1:
                        trainers.remove(trainer)

        parameters_for_template = {
                'trainer': trainers
            }
        self.response.write(relevant_trainer_template.render(parameters_for_template))

# ---------------------------------------------------------
# Insert the submitted request and redirect to homepage
# --------------------------------------------------------

class InsertRequest2(webapp2.RequestHandler):
    def get(self):
        global d_id_req_t
        global d_days_req_t
        global d_part_of_days_req_t
        # Retrieve data from the GET request
        # Using class request - to insert to DB--->???
        request1 = request.request()
        request1.req_status = "Pending"
        request1.req_dog_id = d_id_req_t
        request1.req_email_service_provider = str(self.request.get('trainer_email'))
        request1.req_day = d_days_req_t
        request1.req_part_of_day = d_part_of_days_req_t
        request1.req_creation_time = date.today()
        request1.req_respond_time = date.today()
        request1.insertToDb()
        # Redirects to the Dog Owner homepage
        self.redirect('/homepage_dog_owner')

# ---------------------------------------------------------
# Displays to the service provider the requests sent to him
# allows him to approve them and also presents him with his activity log
# ---------------------------------------------------------

class WorkerRequest(webapp2.RequestHandler):
    def get(self):
        # Create a template object
        worker_request_template = jinja_environment.get_template('homepage_worker.html')
        user = users.get_current_user()
        # Creating a list of all the request
        requests = []
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        # Getting from DB only pending requests
        sql = """SELECT Request_ID, U.Name, D.Name, D.Email, Av_Day, Av_Part_Of_Day
                            FROM Request as R JOIN Dog AS D On R.ID = D.ID
                            JOIN User AS U ON D.Email = U.Email
                            WHERE R.Email = '""" + user.email() + "' and S_P_Answer= 'Pending'; "
        cursor.execute(sql)
        temps = cursor.fetchall()
        # Making a list of all the requests
        for temp in temps:
            temp_dict = {}
            temp_dict['request_id'] = str(temp[0])
            temp_dict['dog_owner_name'] = str(temp[1])
            temp_dict['dog_name'] = str(temp[2])
            temp_dict['dog_owner_email'] = str(temp[3])
            temp_dict['day'] = str(temp[4])
            temp_dict['time'] = str(temp[5])
            requests.append(temp_dict)
        # allows trainer to approve only one train for the same date and time
        if check_if_trainer(user.email()):
            sql = """SELECT Email , COUNT(*), Av_Day, Av_Part_Of_Day 
                                FROM Request
                                 WHERE S_P_Answer='True'
                                  GROUP BY Email, Av_Day, Av_Part_Of_Day;"""
            cursor.execute(sql)
            d_DbHandler.commit()
            temps1 = cursor.fetchall()
            for request in requests:
                for temp1 in temps1:
                    if str(user.email()) == str(temp1[0]):
                        if str(request['day']) == str(temp1[2]) and str(request['time']) == str(temp1[3]):
                            if int(temp1[1]) == 1:
                                requests.remove(request)
        # allows walker to approve up to max dogs amount for the same date and time
        else:
            sql = """SELECT R.Email , COUNT(*), R.Av_Day, R.Av_Part_Of_Day, Max_Dogs 
                                            FROM Request as R join Dog_Walker as W on R.Email=W.Email 
                                             WHERE R.S_P_Answer='True'
                                              GROUP BY R.Email, R.Av_Day, R.Av_Part_Of_Day;"""
            cursor.execute(sql)
            d_DbHandler.commit()
            temps1 = cursor.fetchall()
            for request in requests:
                for temp1 in temps1:
                    if str(user.email()) == str(temp1[0]):
                        if str(request['day']) == str(temp1[2]) and str(request['time']) == str(temp1[3]):
                            if temp1[1] >= (temp1[4]):
                                requests.remove(request)
        # Creating a list of all the booked activities
        activities = []
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        # Getting from DB only approved requests
        sql = """SELECT Request_ID, U.Name, D.Name, D.Email, Av_Day, Av_Part_Of_Day
                                    FROM Request as R JOIN Dog AS D On R.ID = D.ID
                                    JOIN User AS U ON D.Email = U.Email
                                    WHERE R.Email = '""" + user.email() + "' and S_P_Answer= 'True'; "
        cursor.execute(sql)
        d_DbHandler.commit()
        temps2 = cursor.fetchall()
        # Making a list of all the activities
        for temp in temps2:
            temp_dict = {}
            temp_dict['activity_id'] = str(temp[0])
            temp_dict['activity_dog_owner_email'] = str(temp[3])
            temp_dict['activity_dog_owner_name'] = str(temp[1])
            temp_dict['activity_dog_name'] = str(temp[2])
            temp_dict['activity_day'] = str(temp[4])
            temp_dict['activity_time'] = str(temp[5])
            activities.append(temp_dict)

        parameters_for_template = {
            'list_of_requests': requests,
            'list_of_activitys':activities
        }

        self.response.write(worker_request_template.render(parameters_for_template))

# ---------------------------------------------------------
# Update the request status and time according the service provider's answer
# ---------------------------------------------------------

class RespondWorker(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # Retrieve data from the GET request
        d_DbHandler = db_handler.DbHandler()
        cursor = d_DbHandler.getCursor()
        req_status = str(self.request.get('answer_respond'))
        req_dog_id = str(self.request.get('request_answer_id'))
        req_av_day = str(self.request.get('av_day'))
        req_av_time = str(self.request.get('av_time'))
        # Update the request status according to the service provider decision
        sql = """UPDATE Request
                Set S_P_Answer = "%s" ,Date_Of_Answer="%s"
                Where Request_ID="%s" """
        sql = sql % (req_status, date.today(), req_dog_id)
        cursor.execute(sql)
        d_DbHandler.commit()
        #if trainer, update num of trained dogs
        if check_if_trainer(user.email()):
            cursor = d_DbHandler.getCursor()
            sql = """UPDATE Trainer
                    Set Num_Of_Trained_Dogs = Num_Of_Trained_Dogs + 1
                    Where Email ="%s" """
        sql = sql % (user.email())
        cursor.execute(sql)
        d_DbHandler.commit()
        d_DbHandler.disconnectFromDb()
        # Redirects to the next page
        self.redirect('/homepage_worker')

# ---------------------------------------------------------
# Dog owner Homepage
# ---------------------------------------------------------

class DogOwnerHomePage(webapp2.RequestHandler):
    def get(self):
        home_page_template = jinja_environment.get_template('homepage_dog_owner.html')
        self.response.write(home_page_template.render())



app = webapp2.WSGIApplication([('/', MainPage),
                               ('/login', Login),
                               ('/sign_up', FirstLogin),
							   ('/register_dog_owner', DogOwnerRegister),
                               ('/register_dog', AddNewDog),
                               ('/register_dog_walker', DogWalkerRegister),
                               ('/register_trainer', TrainerRegister),
                               ('/homepage_dog_owner',DogOwnerHomePage),
                               ('/homepage_worker', WorkerRequest),
                               ('/walk_request',WalkRequest),
                               ('/Thank_You', InsertRequest),
                               ('/relevant_walker',RelevantWalker),
                               ('/train_request',TrainRequest),
                               ('/relevant_trainer',RelevantTrainer),
                               ('/Thank_You2', InsertRequest2),
                               ('/request_answer',RespondWorker),
							   ('/logout',Logout)],
                              debug=True)