
from interface import Regressor
from utils import get_data
from config import *
import time


start_time = time.time()  # Record the starting time of the pro
class SimpleMean(Regressor):  # A simple baseline model that predicts the mean rating of a user for any item
    def __init__(self):
        self.user_means = {}      # Calculate the mean rating for each user and store it in the user_means dictionary

#  Fit the baseline model to the training data.
    def fit(self, X):
        # Return the mean rating for the given user from the user_means dictionary
        self.user_means = X.groupby(USER_COL_NAME_IN_DATAEST)[RATING_COL_NAME_IN_DATASET].mean().to_dict()

#  Predict the rating for a given user-item pair.
    def predict_on_pair(self, user: int, item: int):
        return self.user_means.get(user)



if __name__ == '__main__':
    train, validation = get_data()  # Obtain the training and validation data using the get_data function
    baseline_model = SimpleMean()  # Create an instance of the SimpleMean baseline model
    baseline_model.fit(train)   # Fit the baseline model to the training data
    print(baseline_model.calculate_rmse(validation))   # Print the root mean squared error (RMSE) of the baseline model


print("--------------------------")
end_time = time.time()  # Record the ending time of the program
total_time = end_time - start_time   # Calculate the total runtime of the program
print("Total runtime: {:.2f} seconds".format(total_time))