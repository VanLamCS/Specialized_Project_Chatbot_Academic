import sys
import json
import os

def findPositionOfSubstring(mainString, subString):
  start = mainString.find(subString)
  if start == -1:
    return (-1, -1)
  else:
    end = start + len(subString)
    if mainString[start : end] == subString:
      return (start, end)
    elif mainString[start - 1 : end - 1] == subString:
      return (start - 1, end - 1)
    elif mainString[start - 2 : end - 2] == subString:
      return (start - 2, end - 2)

def main():
  folder = "./test/data"
  for fileName in os.listdir(folder):
    if fileName.endswith(".json"):
      filePath = os.path.join(folder, fileName)
      with open(filePath, "rb") as f:
        trainObj = json.load(f)
      
      dataTrains = trainObj["data"]
      for i in range(len(dataTrains)):
        answerStart = []
        answerEnd = []
        for answerText in dataTrains[i]["answers"]["text"]:
            position = findPositionOfSubstring(dataTrains[i]["context"], answerText)
            if position[0] != -1 and position[1] != -1:
                answerStart += [position[0]]
                answerEnd += [position[1]]
        dataTrains[i]["answers"]["answer_start"] = answerStart
        dataTrains[i]["answers"]["answer_end"] = answerEnd
      trainObj["data"] = dataTrains
      with open(filePath, "w", encoding="utf-8") as f:
        json.dump(trainObj, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  main()