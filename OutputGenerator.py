import json
import os
import xmltodict
import re
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
        if isinstance(jsonObj, dict):
            f = open(self.getFilePathToWriteJSONLD(), "w")
            f.write(json.dumps(jsonObj, indent=4))
            f.close()
        elif isinstance(jsonObj, list):
            i = 1
            for item in jsonObj:
                f = open(re.sub("[.]", '_'+str(i)+'.', self.getFilePathToWriteJSONLD()), "w")
                f.write(json.dumps(item, indent=4))
                i += 1
                f.close()

    def writeTurtleFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            f = open(self.getFilePathToWriteTurtle(), "w")
            g = Graph().parse(data=str(json.dumps(jsonObj, indent=4)), format='json-ld')
            f.write(g.serialize(format='n3'))
            # print(g.serialize(format='n3'))
            f.close()
        else:
            i = 1
            for item in jsonObj:
                f = open(re.sub("[.]", '_'+str(i)+'.', self.getFilePathToWriteTurtle()), "w")
                g = Graph().parse(data=str(json.dumps(item, indent=4)), format='json-ld')
                f.write(g.serialize(format='n3'))
                i += 1
                f.close()

    def writeOWLFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            f = open(self.getFilePathToWriteOWL(), "w")
            g = Graph().parse(data=str(json.dumps(jsonObj, indent=4)), format='json-ld')
            f.write(g.serialize(format='pretty-xml'))
            f.close()
        else:
            i = 1
            for item in jsonObj:
                f = open(re.sub("[.]", '_'+str(i)+'.', self.getFilePathToWriteOWL()), "w")
                g = Graph().parse(data=str(json.dumps(item, indent=4)), format='json-ld')
                f.write(g.serialize(format='pretty-xml'))
                i += 1
                f.close()
