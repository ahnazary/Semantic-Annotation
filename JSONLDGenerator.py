class JSONLDGenerator():

    def __init__(self, filePath, urisToAdd):
        self.filePath = filePath
        self.urisToAdd = urisToAdd
        self.WriteJSONLDFile()

    def getFileNameToWrite(self):
        if '/' in self.filePath:
            name = self.filePath.split('/')[-1]
        else:
            name = self.filePath
        return name + ".JSONLD"

    def WriteJSONLDFile(self):
        f = open(self.filePath)
        Lines = f.readlines()
        f.close()
        print(self.getNumberOfLinesOfFile())

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
            print(line)

            if lineIndex == self.getNumberOfLinesOfFile()-2:
                finalContent += line
            elif lineIndex == self.getNumberOfLinesOfFile() - 1:
                finalContent += strToAdd + '\n' + line
            else:
                finalContent += line
            lineIndex += 1

        print(finalContent)
        f = open(self.getFileNameToWrite(), "w")
        f.write(finalContent)
        f.close()

    def getNumberOfLinesOfFile(self):
        file = open(self.filePath, "r")
        line_count = 0
        for line in file:
            line_count += 1
        file.close()
        return line_count
