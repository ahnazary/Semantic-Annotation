import json
import os

import xmltodict

from ExtractKeywords import ExtractKeywords
from rdflib import Graph, plugin
from rdflib.serializer import Serializer


class OutputGenerator():

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
        fh = open(self.filePath)
        if self.filePath.split(' ')[-1].split('.')[-1].lower() == 'json':
            lines = fh.read().split('\n')
            f = open(self.getFilePathToWrite(), "w")
            f.write(self.createJSONLDString(lines))
            f.close()
        elif self.filePath.split(' ')[-1].split('.')[-1] == 'xml':
            xmlData = xmltodict.parse(fh.read())
            lines = json.dumps(xmlData, indent=4).split('\n')
            f = open(self.getFilePathToWrite(), "w")
            f.write(self.createJSONLDString(lines))
            f.close()
        else:
            f = open(self.getFilePathToWrite(), "w")
            lines = json.dumps(ExtractKeywords.convertUnstructuredToJson(fh), indent=4).split('\n')
            f.write(self.createJSONLDString(lines))
            f.close()

    def createJSONLDString(self, lines):
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
        for line in lines:
            if lineIndex == len(lines) - 2:
                finalContent += (line + '\n')
            elif lineIndex == len(lines) - 1:
                finalContent += '\n' + strToAdd + '\n' + line
            else:
                finalContent += (line + '\n')
            lineIndex += 1

        return finalContent

    @staticmethod
    def writeRDFFile(inputStr):
        g = Graph().parse(data=inputStr, format='json-ld')
        # print(g.serialize(format='n3'))
        return g.serialize(format='n3')