import json
import uuid


def is_valid_uuid(value):
    try:
        uuid_obj = uuid.UUID(value)
        return True
    except ValueError:
        return False
    

def main():
    datasetBase = "./test/data_v2/"
    print("Input file name: ")
    fileName = input()
    if fileName == "":
        fileName = datasetBase + "train_v1.json"
    else:
        fileName = datasetBase + fileName

    try:
        with open(fileName, "rb") as f:
            trainObj = json.load(f)
        dataTrains = trainObj["data"]

        uniqueId = ""

        for i in range(len(dataTrains)):
            try:
                if not is_valid_uuid(dataTrains[i]["id"]):
                    uniqueId = str(uuid.uuid4())
                    trainObj["data"][i]["id"] = uniqueId
            except Exception as e:
                uniqueId = str(uuid.uuid4())
                trainObj["data"][i]["id"] = uniqueId

        with open(fileName, "w", encoding="utf-8") as f:
            json.dump(trainObj, f, ensure_ascii=False, indent=2)

    except Exception as error:
        raise error


if __name__ == "__main__":
    main()
