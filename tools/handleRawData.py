import sys
import re

class HandleContext:
    def __init__(self, srcPath: str = "", destPath: str = ""):
        self.srcPath = srcPath
        self.destPath = destPath
        self.data = """"""
    
    def setSrcPath(self, srcPath: str):
        self.srcPath = srcPath

    def setDestPath(self, destPath: str):
        self.destPath = destPath
    
    def loadFile(self):
        try:
            with open(self.srcPath, 'r') as file:
                data = file.read()
                self.data = data
                print(f"Read data at '{self.srcPath}' success")
                return data
        except FileNotFoundError:
            print(f"Read file: File '{self.srcPath}' not found.")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""
    def saveFile(self):
        try:
            with open(self.destPath, 'w') as file:
                file.write(self.data)
                print(f"Write data into '{self.destPath}' success")
                return True
        except Exception as e:
            print(f"Write error occurred: {e}")
            return False
    
    def removeDoubleEnter(self):
        cleanedStr = re.sub(r'\n\n+', '\n', self.data)
        self.data = cleanedStr
        return cleanedStr
    
    def removeDoubleSpace(self):
        cleanedStr = re.sub(r'\s+', ' ', self.data)
        self.data = cleanedStr
        return cleanedStr
    
    def removeUnnecessaryLineBreaks(self):
        cleanedStr = re.sub(r'(?<![\.;:])\n', ' ', self.data)
        self.data = cleanedStr
        return cleanedStr

    def addSpacesAround(self):
        charactersToSurround = r'\.\,\(\)\-\/\:\;\{\}\`\^\&\<\=\>\*\+\!\#\$\%\@\~\_\|\[\]\"\'\n\t\?'
        modifiedStr = re.sub(f'([{charactersToSurround}])', r' \1 ', self.data)
        self.data = modifiedStr
        return modifiedStr

    def removeSpaceAroundNumber(self):
        modifiedStr = re.sub(r'\s+(\d+)\s+\.\s+(\d+)\s+', r' \1.\2 ', self.data)
        self.data = modifiedStr
        return modifiedStr
    
    def escapeSomeCharacters(self):
        self.data = self.data.replace('\'', r'\'')
        self.data = self.data.replace('\"', r'\"')
        self.data = self.data.replace('\n', r'\n')
        return self.data
    
    def replaceSomeSpecial(self):
        self.data = self.data.replace(r', . . .', r',...')
        self.data = self.data.replace(r'. . .', r'...')
        return self.data

    def updateContext(self):
        self.removeDoubleEnter()
        self.removeUnnecessaryLineBreaks()
        self.addSpacesAround()
        self.escapeSomeCharacters()
        self.removeSpaceAroundNumber()
        self.removeDoubleSpace()
        self.replaceSomeSpecial()
    
    def printContext(self):
        showData = self.data.replace(r'\n', '\n')
        self.data = showData
        return showData

if __name__ == "__main__":
    if(len(sys.argv) <= 2):
        print("-----Require-----\nParam 1: source path\nParam 2: destination path")
    else: 
        srcPath = sys.argv[1]
        destPath = sys.argv[2]
        handleCtx = HandleContext(srcPath, destPath)
        handleCtx.loadFile()
        handleCtx.updateContext()
        handleCtx.saveFile()
        