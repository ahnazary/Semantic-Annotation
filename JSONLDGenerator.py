import os


class JSONLDGenerator():

    def __init__(self, filePath, urisToAdd):
        self.filePath = filePath
        self.urisToAdd = urisToAdd

    def getFilePathToWrite(self):
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if '/' in self.filePath:
            name = self.filePath.split('/')[-1]
            name = name.split('.')[0] + ".JSONLD"
        else:
            name = self.filePath

        completeName = os.path.join(projectPath + "/JSONLDs", name)
        return completeName

    def WriteJSONLDFile(self):
        f = open(self.filePath)
        Lines = f.readlines()
        f.close()

        strToAdd = ""
        if len(self.urisToAdd) == 0:
            strToAdd = "   @context\": [ ]"
        elif len(self.urisToAdd) > 0:
            strToAdd = "   @context\": [ \n"
            num = 0
            for i in self.urisToAdd:
                num += 1
                if num != len(self.urisToAdd):
                    strToAdd += '    \"' + i + '\",\n'
                if num == len(self.urisToAdd):
                    strToAdd += '    \"' + i + '\"\n'
            strToAdd += '   ]'

        finalContent = ""
        lineIndex = 0
        for line in Lines:
            if lineIndex == self.getNumberOfLinesOfFile()-2:
                finalContent += line
            elif lineIndex == self.getNumberOfLinesOfFile() - 1:
                finalContent += strToAdd + '\n' + line
            else:
                finalContent += line
            lineIndex += 1

        f = open(self.getFilePathToWrite(), "w")
        f.write(finalContent)
        f.close()

    def getNumberOfLinesOfFile(self):
        file = open(self.filePath, "r")
        line_count = 0
        for line in file:
            line_count += 1
        file.close()
        return line_count
