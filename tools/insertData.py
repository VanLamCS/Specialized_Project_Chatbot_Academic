""" Add some questions that have the same answer as the existing questions  """

import os
import json
import uuid

# These constants can be changed appropriately
DEST_DIR = "test/data"
ADD_DIR = "test/upgradeData"
DATA_VERSION = "1.0.2"


def read_file(folder_path, file_name):
    try:
        with open(os.path.join(folder_path, file_name), "rb") as f:
            data = json.load(f)
        return data
    except Exception as e:
        return []


def write_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_element_by_id(data, target_id):
    for element in data:
        if element["id"] == target_id:
            return element
    return None


def is_question_exists(list_of_array_questions, question):
    for list_questions in list_of_array_questions:
        for item in list_questions:
            if question == item["question"]:
                return True
    return False


def generate_elements(
    questions_in_origin, add_data_generated, template_element, list_question
):
    if template_element is None:
        return []
    questions_generated = []
    for question in list_question:
        if not is_question_exists(
            [add_data_generated, questions_generated, questions_in_origin], question
        ):
            new_id = str(uuid.uuid4())
            element_copied = template_element.copy()
            element_copied["id"] = new_id
            element_copied["question"] = question
            questions_generated.append(element_copied)
        else:
            print("Already exists:", question)
    return questions_generated


def combine_data(origin_data, add_data, data_version=DATA_VERSION):
    origin_data["version"] = data_version
    origin_data["data"] += add_data
    return origin_data


def main():
    add_files = os.listdir(ADD_DIR)
    dest_files = os.listdir(DEST_DIR)

    files_modified = []
    total_add = 0

    for add_file_name in add_files:
        if add_file_name.endswith(".json") and add_file_name in dest_files:
            add_data_generated = []
            add_data = read_file(ADD_DIR, add_file_name)
            dest_data = read_file(DEST_DIR, add_file_name)
            if (
                not isinstance(add_data, list)
                and not add_data.strip()
                or len(add_data) == 0
            ):
                continue
            for set in add_data:
                template_element = find_element_by_id(dest_data["data"], set["id"])
                questions_generated = generate_elements(
                    dest_data["data"],
                    add_data_generated,
                    template_element,
                    set["questions"],
                )
                add_data_generated += questions_generated
            size_of_generation = len(add_data_generated)
            if size_of_generation > 0:
                new_data = combine_data(dest_data, add_data_generated)
                write_file(os.path.join(DEST_DIR, add_file_name), new_data)
                files_modified.append(add_file_name)
                total_add += size_of_generation

    print("==========")
    print("Files were modified:", files_modified)
    print("Number of questions added:", total_add)


if __name__ == "__main__":
    main()
