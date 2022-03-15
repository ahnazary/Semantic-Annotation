import json
import os
import xmltodict
from ExtractKeywords import ExtractKeywords
from rdflib import Graph


class OutputGenerator:

    def __init__(self, filePath, urisToAdd):
        self.filePath = filePath
        self.urisToAdd = urisToAdd

    def getFilePathToWriteJSONLD(self):
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if '/' in self.filePath:
            name = self.filePath.split('/')[-1]
            name = name.split('.')[0] + ".JSONLD"
        else:
            name = self.filePath

        completeName = os.path.join(projectPath + "/Outputs", name)
        return completeName

    def getFilePathToWriteTurtle(self):
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if '/' in self.filePath:
            name = self.filePath.split('/')[-1]
            name = name.split('.')[0] + ".ttl"
        else:
            name = self.filePath

        completeName = os.path.join(projectPath + "/Outputs", name)
        return completeName

    def getFilePathToWriteOWL(self):
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if '/' in self.filePath:
            name = self.filePath.split('/')[-1]
            name = name.split('.')[0] + ".xml"
        else:
            name = self.filePath

        completeName = os.path.join(projectPath + "/Outputs", name)
        return completeName

    def writeJSONLDFileFromDict(self, jsonObj):
        f = open(self.getFilePathToWriteJSONLD(), "w")
        f.write(json.dumps(jsonObj, indent=4))
        f.close()

    def writeJSONLDFile(self):
        fh = open(self.filePath)
        if self.filePath.split(' ')[-1].split('.')[-1].lower() == 'json':
            jsonObj = json.load(fh)
            f = open(self.getFilePathToWriteJSONLD(), "w")
            f.write(json.dumps(jsonObj, indent=4))
            f.close()
        elif self.filePath.split(' ')[-1].split('.')[-1] == 'xml':
            xmlData = xmltodict.parse(fh.read())
            f = open(self.getFilePathToWriteJSONLD(), "w")
            f.write(json.dumps(xmlData, indent=4))
            f.close()
        else:
            f = open(self.getFilePathToWriteJSONLD(), "w")
            f.write(json.dumps(ExtractKeywords.convertUnstructuredToJson(fh), indent=4))
            f.close()

    def writeTurtleFile(self, inputStr):
        f = open(self.getFilePathToWriteTurtle(), "w")
        g = Graph().parse(data=inputStr, format='json-ld')
        print(inputStr)
        print(g.serialize(format="json-ld"))
        print(g.serialize(format="n3"))
        f.write(g.serialize(format='n3'))
        f.close()

    def writeOWLFile(self, inputStr):
        f = open(self.getFilePathToWriteOWL(), "w")
        g = Graph().parse(data=inputStr, format='json-ld')
        f.write(g.serialize(format='pretty-xml'))
        f.close()