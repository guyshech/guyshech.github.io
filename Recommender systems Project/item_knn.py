#  Imports:
import numpy as np
from numpy import sqrt
import itertools
import pandas as pd
from interface import Regressor
from utils import get_data, Config
from tqdm import tqdm
from scipy.sparse import csr_matrix
from scipy.sparse import coo_matrix
from pathlib import Path
from config import CORRELATION_PARAMS_FILE_PATH, CSV_COLUMN_NAMES, VALIDATION_PATH
import csv
import time
validation_data = pd.read_csv(VALIDATION_PATH)

start_time = time.time()

#  defines a class named KnnItemSimilarity, which inherits from the Regressor class
class KnnItemSimilarity(Regressor):
    def __init__(self, config):
        self.sim_dict = {}
        self.save_lst = []
        self.mean_item_rate = None
        self.user_item_matrix = None
        self.k = config.k
        self.num_items = None
        self.num_users = None


    def fit(self, X: np.array):
        # Extract users, items, and ratings from the training data
        users = np.array(X['User_ID_Alias'])
        items = np.array(X['Movie_ID_Alias'])
        ratings = np.array(X['Ratings_Rating'])
        self.num_users = len(X['User_ID_Alias'].unique())
        self.num_items = len(X['Movie_ID_Alias'].unique())

        # Create a user-item matrix from the training data
        max_users = max(len(validation_data["User_ID_Alias"].unique()), self.num_users)
        max_items = max(len(validation_data["Movie_ID_Alias"].unique()), self.num_items)

        # sparse matrix (csr_matrix) is constructed using the ratings, users, and items arrays. The matrix is
        self.user_item_matrix = csr_matrix((ratings, (users, items)), shape=(max_users, max_items),
                                           dtype=np.int16).toarray()
        self.user_item_matrix = self.user_item_matrix.astype('float')
        # zeros in the array are replaced with 'nan' values.
        self.user_item_matrix[self.user_item_matrix == 0] = 'nan'
        self.mean_item_rate = np.nanmean(self.user_item_matrix, axis=0)

        if Path(CORRELATION_PARAMS_FILE_PATH).exists():  # if we already created a file with the saved parameters take the parameters from the file
            self.upload_params()
        else:  # if its the first time calculate item_to_item_corr_dict
            self.build_item_to_item_corr_dict(X)
            self.save_params()

    def build_item_to_item_corr_dict(self, data):
        # Generate all possible pairs of item indices using itertools combinations
        all_items_pairs = list(itertools.combinations(range(self.num_items), 2))
        for pair in tqdm(all_items_pairs):  # for each pair of items
            item1, item2 = pair[0], pair[1]
            item_to_item = self.user_item_matrix[:, item1] * self.user_item_matrix[:, item2].T  # multiply item1 and item2 vectors to find the common items both of them rated
            is_none = np.isnan(item_to_item)
            p = np.where(is_none == False)[0].tolist()  # p represents the userss that have ratings from both item1 and item2
            if len(p) >= 2:  # if both of the items rated more than 2 users
                # Retrieve the mean ratings for item1 and item2
                item1_mean_rating = self.mean_item_rate[item1]
                item2_mean_rating = self.mean_item_rate[item2]
                # Compute the deviations of ratings from the mean ratings for item1 and item2
                item1_part = self.user_item_matrix[p, item1] - item1_mean_rating
                item2_part = self.user_item_matrix[p, item2] - item2_mean_rating
                # calculate pearson correlation
                upper = np.sum(item1_part * item2_part.T)
                lower = sqrt((item1_part ** 2).sum()) * sqrt((item2_part ** 2).sum())
                if lower != 0 and upper > 0:  # calculate the pearson correlation only for positive values
                    self.save_lst.append([pair, upper/lower])
                    self.sim_dict[pair] = upper/lower
                    t1 = (item2, (upper / lower))
                    t2 = (item1, (upper / lower))
                    if item1 in self.sim_dict:
                        self.sim_dict[item1].append(t1)
                    else:
                        self.sim_dict[item1] = [t1]  # Append the correlation value to item1's similarity list
                    if item2 in self.sim_dict:
                        self.sim_dict[item2].append(t2)
                    else:
                        self.sim_dict[item2] = [t2]  # Append the correlation value to item2's similarity list


    def predict_on_pair(self, user, item):  # predicts the rating for a user-item pair
        if item in self.sim_dict:
            sim_per_item = self.sim_dict[int(item)]
            # Check if the number of similarity values is greater than k
            if len(sim_per_item) > self.k:
                sim_per_item = np.array([item[1] for item in sim_per_item])
                # Find the indices of the top k similarity values using argsort
                k_index = np.argsort(sim_per_item)[(len(sim_per_item) - self.k):]
            else:
                k_index = sim_per_item  # Use all similarity values if there are fewer than k values available
            upper, lower = 0, 0
            # Run over the indices of the top k similarity values
            for i in k_index:
                if self.sim_dict[int(item)][i][1] != 0:  # Check if the similarity value is not zero
                    # calculate the pearson similarity
                    sim = self.sim_dict[int(item)][i][1]
                    rating = self.user_item_matrix[int(user), i]
                    upper += (sim * rating)
                    lower += sim
            # Check if both of them are positive
            if (upper > 0) & (lower > 0):
                return upper / lower
            else:
                return self.mean_item_rate[int(item)]
        # If the item is not in sim_dict we will want to ignore him in the total calculation for the RMSE
        else:
            for row in validation:
                val_user, val_item, val_rating = row
                if val_user == user and val_item == item:
                    # by returning the value from the validation the addition to the total RMSE will be 0
                    return val_rating

    #  The upload_params() method is responsible for loading the correlation parameters from a CSV file
    def upload_params(self):
        # It reads the CSV file, retrieves the item pairs, correlations, and saves them into sim_dict
        data = pd.read_csv(CORRELATION_PARAMS_FILE_PATH)
        item1 = np.array(data[CSV_COLUMN_NAMES[0]])
        item2 = np.array(data[CSV_COLUMN_NAMES[1]])
        s = np.array(data[CSV_COLUMN_NAMES[2]])
        # sim_dict is structured such that for each item, there is a list of tuples containing the correlated items and their corresponding correlations
        for i in range(len(item1)):
            if item1[i] in self.sim_dict:
                self.sim_dict[item1[i]].append((item2[i], s[i]))
            else:
                self.sim_dict[item1[i]] = [(item2[i], s[i])]
            if item2[i] in self.sim_dict:
                self.sim_dict[item2[i]].append((item1[i], s[i]))
            else:
                self.sim_dict[item2[i]] = [(item1[i], s[i])]

    #  The save_params() method is responsible for saving the correlation parameters to a CSV file.
    def save_params(self):
        with open(CORRELATION_PARAMS_FILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_COLUMN_NAMES)   # Write header row
            for l in self.save_lst:
                # converts the values to the appropriate data types
                item1 = l[0][0]
                item2 = l[0][1]
                ranking = l[1]
                r_ranking = round(ranking, 3)  # rounds the correlation value to three decimal places
                row = (item1, item2, r_ranking)
                writer.writerow(row)


if __name__ == '__main__':
    knn_config = Config(k=25)
    train, validation = get_data()
    knn = KnnItemSimilarity(knn_config)
    knn.fit(train)
    print(knn.calculate_rmse(validation))


# Your model training code here
print("--------------------------")
end_time = time.time()
total_time = end_time - start_time
print("Total runtime: {:.2f} seconds".format(total_time))
