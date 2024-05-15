import numpy as np
import time
from numpy import sqrt
import itertools
import pandas as pd
from interface import Regressor
from utils import get_data, Config
from tqdm import tqdm
from scipy.sparse import csr_matrix
from pathlib import Path
from config import CSV_COLUMN_NAMES, VALIDATION_PATH
import csv
validation_data = pd.read_csv(VALIDATION_PATH)
CORRELATION_USERS_FILE_PATH = "learned_paramaters/correlation_users.csv"
start_time = time.time()

# This class inherits from the Regressor class
class KnnUserSimilarity(Regressor):
    def __init__(self, config):
        self.sim_dict = {}
        self.save_lst = []
        self.mean_user_rate = None
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
        edit_ratings = np.zeros((max_users, max_items))
        for i in range(len(users)):
            edit_ratings[items[i], users[i]] = ratings[i]

        # Compute mean user rating and item means
        self.user_item_matrix = csr_matrix(edit_ratings, dtype=np.int16).toarray()
        self.user_item_matrix = self.user_item_matrix.astype('float')
        self.user_item_matrix[self.user_item_matrix == 0] = 'nan'

        # Compute mean user rating, item means and user means without considering null values
        self.mean_user_rate = np.nanmean(self.user_item_matrix, axis=0)

        # Build user-to-user correlation dictionary from the matrix
        self.build_user_to_user_corr_dict()
        if Path(CORRELATION_USERS_FILE_PATH).exists():  # if we already created a file with the saved parameters take the parameters from the file
            self.upload_params()
        else:  # if its the first time calculate item_to_item_corr_dict
            self.build_user_to_user_corr_dict()
           # save params method -we put here the function "save params" because this method wasnt in the file we recived for the project
            with open(CORRELATION_USERS_FILE_PATH, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(CSV_COLUMN_NAMES)  # Write header row
                for l in self.save_lst:
                    # converts the values to the appropriate data types
                    user1 = l[0][0]
                    user2 = l[0][1]
                    ranking = l[1]
                    r_ranking = round(ranking, 3)  # rounds the correlation value to three decimal places
                    row = (user1, user2, r_ranking)
                    writer.writerow(row)

    def build_user_to_user_corr_dict(self):
        # Generate all possible pairs of user indices using itertools combinations
        possible_pairs = list(itertools.combinations(range(self.num_users), 2))
        for pair in tqdm(possible_pairs):  # for each pair of users
            user1, user2 = pair[0], pair[1]
            user_to_user = self.user_item_matrix[:, user1] * self.user_item_matrix[:, user2].T  # multiply user1 and user2 vectors to find the common items both of them rated
            is_none = np.isnan(user_to_user)
            p = np.where(is_none == False)[0].tolist()  # p represents the items that have ratings from both user1 and user2
            if len(p) >= 2:  # if both of the users rated more than 2 items

                user1_mean_rating, user2_mean_rating = self.mean_user_rate[user1], self.mean_user_rate[user2]  # Retrieve the mean ratings for user1 and user2
                if None in [user1_mean_rating, user2_mean_rating]:
                    # Skip if any of the mean ratings is None (missing value)
                    continue
                else:
                    # Compute the deviations of ratings from the mean ratings for user1 and user2
                    user1_part = self.user_item_matrix[p, user1] - user1_mean_rating
                    user2_part = self.user_item_matrix[p, user2] - user2_mean_rating
                    # calculate pearson correlation
                    upper = np.sum(user1_part * user2_part.T)
                    lower = sqrt((user1_part ** 2).sum()) * sqrt((user2_part ** 2).sum())

                    if lower != 0 and upper > 0:  # calculate the pearson correlation only for positive values
                        self.save_lst.append([pair, upper/lower])
                        t1 = (user2, (upper / lower))
                        t2 = (user1, (upper / lower))
                        if user1 in self.sim_dict:
                            self.sim_dict[user1].append(t1)
                        else:
                            # Append the correlation value to user1's similarity list
                            self.sim_dict[user1] = [t1]
                        if user2 in self.sim_dict:
                            self.sim_dict[user2].append(t2)
                        else:
                            # Append the correlation value to user2's similarity list
                            self.sim_dict[user2] = [t2]

    def predict_on_pair(self, user: int, item: int):
        if user in self.sim_dict:
            sim_per_user = self.sim_dict[int(user)]
            # Check if the number of similarity values is greater than k
            if len(sim_per_user) > self.k:
                sim_per_user = np.array([user[1] for user in sim_per_user])
                # Find the indices of the top k similarity values using argsort
                k_index = np.argsort(sim_per_user)[(len(sim_per_user) - self.k):]
            else:
                # Use all similarity values if there are fewer than k values available
                k_index = sim_per_user
            upper, lower = 0, 0
            # Run over the indices of the top k similarity values
            for i in k_index:
                # Check if the similarity value is not zero
                if self.sim_dict[int(user)][i][1] != 0:
                    # calculate the pearson similarity
                    sim = self.sim_dict[int(user)][i][1]
                    rating = self.user_item_matrix[int(item), i]
                    upper += (sim * rating)
                    lower += sim
            # Check if both of them are positive
            if (upper > 0) & (lower > 0):
                return upper / lower
            else:
                return self.mean_user_rate[int(user)]
        # If the user is not in sim_dict we will want to ignore him in the total calculation for the RMSE
        else:
            for row in validation:
                val_user, val_item, val_rating = row
                if val_user == user and val_item == item:  # Check if the current row matches the target user and item
                    return val_rating



    def upload_params(self):
        # It reads the CSV file, retrieves the item pairs, correlations, and saves them into sim_dict
        data = pd.read_csv(CORRELATION_USERS_FILE_PATH)
        user1 = np.array(data[CSV_COLUMN_NAMES[0]])
        user2 = np.array(data[CSV_COLUMN_NAMES[1]])
        s = np.array(data[CSV_COLUMN_NAMES[2]])
        # sim_dict is structured such that for each item, there is a list of tuples containing the correlated items and their corresponding correlations
        for i in range(len(user1)):
            if user1[i] in self.sim_dict:
                self.sim_dict[user1[i]].append((user2[i], s[i]))
            else:
                self.sim_dict[user1[i]] = [(user2[i], s[i])]
            if user2[i] in self.sim_dict:
                self.sim_dict[user2[i]].append((user1[i], s[i]))
            else:
                self.sim_dict[user2[i]] = [(user1[i], s[i])]




if __name__ == '__main__':
    knn_config = Config(k=10)
    train, validation = get_data()
    train = train.iloc[:200000, :]
    knn = KnnUserSimilarity(knn_config)
    knn.fit(train)
    print(knn.calculate_rmse(validation))


print("--------------------------")
end_time = time.time()
total_time = end_time - start_time
print("Total runtime: {:.2f} seconds".format(total_time))
