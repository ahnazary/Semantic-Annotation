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
            jsonObj = json.load(fh)
            f = open(self.getFilePathToWrite(), "w")
            f.write(self.createJSONLDString(jsonObj))
            f.close()
        elif self.filePath.split(' ')[-1].split('.')[-1] == 'xml':
            xmlData = xmltodict.parse(fh.read())
            f = open(self.getFilePathToWrite(), "w")
            f.write(self.createJSONLDString(xmlData))
            f.close()
        else:
            f = open(self.getFilePathToWrite(), "w")
            f.write(self.createJSONLDString(ExtractKeywords.convertUnstructuredToJson(fh)))
            f.close()

    def createJSONLDString(self, jsonObj):
        jsonObj["@context"] = self.urisToAdd
        result = json.dumps(jsonObj, indent=4)
        return result

    @staticmethod
    def writeRDFFile(inputStr):
        inputStr ="""
                {
          "id": "Actuator:valve1",
           "type": "Actuator",
           "locatedIn":{
                "type": "Relationship",
                "value": [
                    "Building:01",
                    "Zone:02"
                ]
            },
            "hasSensor": {
                "type": "Relationship",
                "value":"Sensor:01"
            }
        }
        """
        context = {}
        context["@vocab"] = "http://purl.org/dc/terms/"
        context["@language"] = "en"
        print(context)

        g = Graph().parse(data=inputStr, format='json-ld')
        print(g.serialize(format='json-ld', context=context, indent=4))
        # print(g.serialize(format='n3'))
        return g.serialize(format='n3')