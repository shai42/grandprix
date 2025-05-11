import pickle
import os

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return []

def save_data(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
