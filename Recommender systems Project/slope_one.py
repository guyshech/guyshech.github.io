#  Imports:
from interface import Regressor
from utils import get_data
from tqdm import tqdm
from config import *
import pickle
import numpy as np
from os import path
from scipy.sparse import csr_matrix
import pandas as pd
import time

# Load validation data from a CSV file
POPULARITY_DIFFERENCES_PARAMS_FILE_PATH = 'learned_paramaters/popularity_differences.pickle'
validation_data = pd.read_csv(VALIDATION_PATH)


# Measure the start time of the script
start_time = time.time()


class SlopeOne(Regressor):
    def __init__(self):
        self.popularity_differences = {}   # Dictionary to store popularity differences between items
        self.user_item_matrix = None  # Matrix representing user-item ratings
        self.num_items = None  # Number of items
        self.num_users = None  # Number of users

    # Fit the model to the training data
    def fit(self, X: np.array):
        # Training data containing User ID, Item ID, and Ratings
        users = np.array(X['User_ID_Alias'])  # Extracting user IDs from the training data
        items = np.array(X['Movie_ID_Alias'])  # Extracting item IDs from the training data
        ratings = np.array(X['Ratings_Rating'])  # Extracting ratings from the training data


        self.num_users = len(X['User_ID_Alias'].unique())  # Counting the number of unique users
        self.num_items = len(X['Movie_ID_Alias'].unique())  # Counting the number of unique items

        # Determine the maximum number of users and items (considering both training and validation data)
        max_users = max(len(validation_data["User_ID_Alias"].unique()), self.num_users)
        max_items = max(len(validation_data["Movie_ID_Alias"].unique()), self.num_items)

        # Create a sparse matrix to represent the user-item ratings
        self.user_item_matrix = csr_matrix((ratings, (users, items)), shape=(max_users, max_items),
                                           dtype=np.int16).toarray()
        self.user_item_matrix = self.user_item_matrix.astype('float')
        self.user_item_matrix[self.user_item_matrix == 0] = 'nan'

        # Check if the file containing learned parameters exists
        if path.exists(POPULARITY_DIFFERENCES_PARAMS_FILE_PATH):
            self.upload_params()
        else:
            self.build_popularity_difference_dict(X)
            self.save_params()


#  Build the popularity difference dictionary based on the user-item matrix.
    def build_popularity_difference_dict(self, data):

        # Iterate over all pairs of items in the user-item matrix
        for i in tqdm(range(self.user_item_matrix.shape[1] - 1)):
            for j in range(i + 1, self.user_item_matrix.shape[1]):
                # Extract the user-item matrix for the current pair of items
                ij_mat = self.user_item_matrix[:, [i, j]].copy()
                # Remove rows where both items have not been rated by any user
                ij_mat = ij_mat[(ij_mat > 0).all(axis=1)]
                # Calculate the number of common users who have rated both items
                c_ij = ij_mat.shape[0]
                # If there are common users who have rated both items
                if c_ij > 0:
                    # Calculate the average popularity difference between the items
                    pd_ij = (ij_mat[:, 0] - ij_mat[:, 1]).mean()
                    # Check if the popularity difference entry already exists in the dictionary
                    if (i, j) not in self.popularity_differences and (j, i) not in self.popularity_differences:
                        # Store the popularity difference and the count in the dictionary
                        self.popularity_differences[(i, j)] = (pd_ij, c_ij)

    def predict_on_pair(self, user: int, item: int):
        # Initialize variables to store the numerator and denominator of the predicted rating
        r_ui, total_c = 0, 0
        # Iterate over all items in the user-item matrix
        for x in range(self.user_item_matrix.shape[1]):
            # Check if the popularity difference entry exists for the pair (item, x)
            if x != item and self.user_item_matrix[user, x] > 0:
                if (item, x) in self.popularity_differences:
                    p_d, c = self.popularity_differences[(item, x)]
                    # Calculate the partial contribution to the numerator of the predicted rating
                    r_ui += (p_d + self.user_item_matrix[user, x]) * c
                    # Accumulate the count for the denominator of the predicted rating
                    total_c += c
                # Check if the popularity difference entry exists for the pair (x, item)
                elif (x, item) in self.popularity_differences:
                    neg_p_d, c = self.popularity_differences[(x, item)]
                    # Invert the popularity difference for the pair (x, item)
                    p_d = -neg_p_d
                    # Calculate the partial contribution to the numerator of the predicted rating
                    r_ui += (p_d + self.user_item_matrix[user, x]) * c
                    # Accumulate the count for the denominator of the predicted rating
                    total_c += c
        return r_ui / total_c


    def upload_params(self):
        # Open the file containing the learned parameters in read mode
        with open(POPULARITY_DIFFERENCES_PARAMS_FILE_PATH, 'rb') as f:
            self.popularity_differences = pickle.load(f)


    def save_params(self):
        # Open the file to write the parameters in binary mode
        with open(POPULARITY_DIFFERENCES_PARAMS_FILE_PATH, 'wb') as f:
            pickle.dump(self.popularity_differences, f)



if __name__ == '__main__':
    train, validation = get_data()
    slope_one = SlopeOne()
    slope_one.fit(train)
    print(slope_one.calculate_rmse(validation))

print("--------------------------")
end_time = time.time()
total_time = end_time - start_time
print("Total runtime: {:.2f} seconds".format(total_time))