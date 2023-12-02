from read_folder_data import *
import sys

sys.path.append("src/")
from config import context_config
import constants

# def get_all_contexts_from_train_files(path_to_data = constants.DATASET_FOLDER):
#     list_of_objects = read_folder_data(path_to_data)
#     seen_contexts = {}
#     unique_objects = []

#     for obj in list_of_objects:
#         context = obj['context']
#         if context not in seen_contexts:
#             obj.pop('id')
#             obj.pop('question')
#             obj.pop('answers')
#             unique_objects.append(obj)
#             seen_contexts[context] = True
#     return unique_objects


def get_all_contexts(file_path=constants.ALL_CONTEXT_FILE):
    with open(file_path, "rb") as f:
        data = json.load(f)
    all_contexts = data["contexts"]
    return all_contexts


def get_contexts_by_key(filter_key: int):
    all_contexts = get_all_contexts()
    context_types = context_config.context_types
    title = ""
    for item in context_types:
        if filter_key == item["context_key"]:
            title = item["title"]
            break
    res_contexts = []
    for item in all_contexts:
        if item["title"] == title:
            res_contexts.append(item["context"])
    return res_contexts
