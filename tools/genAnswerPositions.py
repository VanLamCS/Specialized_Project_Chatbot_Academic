import json
from countTokenPosition import countTokenPosition


def main():
    datasetBase = "./test/data/"
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

        for i in range(len(dataTrains)):
            answerStart = []
            answerEnd = []
            for answerText in dataTrains[i]["answers"]["text"]:
                position = countTokenPosition(dataTrains[i]["context"], answerText)
                if position[0] != -1 and position[1] != -1:
                    answerStart += [position[0]]
                    answerEnd += [position[1]]
            dataTrains[i]["answers"]["answer_start"] = answerStart
            dataTrains[i]["answers"]["answer_end"] = answerEnd

        trainObj["data"] = dataTrains
        with open(fileName, "w", encoding="utf-8") as f:
            json.dump(trainObj, f, ensure_ascii=False, indent=2)

    except Exception as error:
        raise error


if __name__ == "__main__":
    main()
