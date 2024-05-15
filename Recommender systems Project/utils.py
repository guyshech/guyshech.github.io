import pandas as pd
import numpy as np
from config import TRAIN_PATH, VALIDATION_PATH, USER_COL_NAME_IN_DATAEST, ITEM_COL_NAME_IN_DATASET

def get_data():
    """
    reads train, validation to python indices so we don't need to deal with it in each algorithm.
    of course, we 'learn' the indices (a mapping from the old indices to the new ones) only on the train set.
    if in the validation set there is an index that does not appear in the train set then we can put np.nan or
     other indicator that tells us that.
    """

    train = pd.read_csv(TRAIN_PATH)
    validation = pd.read_csv(VALIDATION_PATH)
    train[USER_COL_NAME_IN_DATAEST] = train[USER_COL_NAME_IN_DATAEST] - 1
    train_lst_movie = list(train[ITEM_COL_NAME_IN_DATASET].unique())
    sort_train_lst_movie = sorted(train_lst_movie)
    items_index = list(range(len(sort_train_lst_movie)))
    train[ITEM_COL_NAME_IN_DATASET].replace(sort_train_lst_movie, items_index, inplace=True)
    validation[USER_COL_NAME_IN_DATAEST] = validation[USER_COL_NAME_IN_DATAEST] - 1
    new_movie_index = validation[validation[ITEM_COL_NAME_IN_DATASET].isin(train_lst_movie) == False]
    validation[ITEM_COL_NAME_IN_DATASET][new_movie_index.index] = 0
    validation[ITEM_COL_NAME_IN_DATASET].replace(sort_train_lst_movie, items_index, inplace=True)
    valid_array = np.array(validation)
    return train, valid_array
    # return train, validation



class Config:
    def __init__(self, **kwargs):
        self._set_attributes(kwargs)

    def _set_attributes(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
