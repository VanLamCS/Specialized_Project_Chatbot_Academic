import os
import json

def read_folder_data(folder):
    jsonFiles = []
    for fileName in os.listdir(folder):
        if fileName.endswith('.json'):
            filePath = os.path.join(folder, fileName)
            with open(filePath, 'rb') as f:
                fileData = json.load(f)
                jsonFiles.append(fileData)

    data = []
    for f in jsonFiles:
        data += f['data']
    return data