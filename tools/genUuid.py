import json
import uuid

def main():
  datasetBase = "./dataset/"
  print("Input file name: ")
  fileName = input()
  if fileName == "":
    fileName = datasetBase + "train_v1.json"
  else:
    fileName = datasetBase + fileName
  
  try:
    with open(fileName, "r") as f:
      trainObj = json.load(f)
    dataTrains = trainObj["train"]["data"]

    uniqueId = ""

    for i in range(len(dataTrains)):
      if dataTrains[i]["id"] == "":
        uniqueId = str(uuid.uuid4())
        trainObj["train"]["data"][i]["id"] = uniqueId

    with open(fileName, "w", encoding='utf-8') as f:
      json.dump(trainObj, f, ensure_ascii = False, indent = 2) 
  
  except Exception as error:
    raise error
  
if __name__ == "__main__":
  main()