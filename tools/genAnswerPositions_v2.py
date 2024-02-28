import json
import sys

templateJsonFile = {
  "version": "2.1.0",
  "data": [
    {
      "title": "",
      "context": "",
      "qas": [
        {
          "question": [
            "Câu hỏi số 1",
            "Câu hỏi số 2",
            "Câu hỏi số 3"
          ],
          "answer": {
            "text": "",
            "answer_start": 0,
            "answer_end": 1
          }
        }
      ]
    }
  ]
}

def openJsonFile(path: str):
    try: 
        if path.endswith('.json'):
            with open(path, 'rb') as file:
                data = json.load(file)
            return data
        else:
            raise Exception('Not a json file')
    except Exception as e:
        print(f'Open file: Error occurred {e}')


def saveJsonFile(path: str, data):
    try: 
        if path.endswith('.json'):
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        else:
            raise Exception('Not a json file')
    except Exception as e:
        print(f'Save file: Error occurred {e}')

def findSubstringPosition(mainString: str, subString: str):
    startPosition = mainString.find(subString)
    endPosition = startPosition + len(subString) if startPosition != -1 else -1
    return startPosition, endPosition

def genPositions(data: list):
    for dataItem in data:
        for qa in dataItem['qas']:
            s, e = findSubstringPosition(dataItem['context'], qa['answer']['text'])
            qa['answer']['answer_start'] = s
            qa['answer']['answer_end'] = e
    return data



if __name__ == "__main__":
    if(len(sys.argv) <= 1):
        print("-----Require-----\nParam 1: Json file path")
    else: 
        path = sys.argv[1]
        dataObj = openJsonFile(path)
        data = dataObj['data']
        dataObj['data'] = genPositions(data)
        saveJsonFile(path, dataObj)
        