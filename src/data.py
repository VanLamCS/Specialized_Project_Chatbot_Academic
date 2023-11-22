import os
import json
from sklearn.model_selection import train_test_split
from utils import read_folder_data
from constants import *

def save_data(data, name):
    with open(os.path.join(DATASET_FOLDER + "/merge_dataset/", name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent= 4)
    return


if __name__ == "__main__":
    all_data = read_folder_data.read_folder_data(DATASET_FOLDER)

    train_data, valid_data  = train_test_split(all_data, test_size= 0.1)

    train_data = {"data": train_data}
    valid_data = {"data": valid_data}

    save_data(train_data, "new_train")
    save_data(valid_data, "validation")