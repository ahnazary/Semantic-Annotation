import json
import os
import pprint
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

    def writeJSONLDFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            f = open(self.getFilePathToWriteJSONLD(), "w")
            f.write(json.dumps(jsonObj, indent=4))
            f.close()

        # for when we have multiple files to be annotated, mainly for CSV files
        elif isinstance(jsonObj, list):
            i = 1
            for item in jsonObj:
                f = open(re.sub("[.]", '_'+str(i)+'.', self.getFilePathToWriteJSONLD()), "w")
                f.write(json.dumps(item, indent=4))
                i += 1
                f.close()

    # returns a jsonld formatted result for the API
    def getJSONLDFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            return json.dumps(jsonObj, indent=4)

        # for when we have multiple files to be annotated, mainly for CSV files
        elif isinstance(jsonObj, list):
            result = {}
            i = 1
            for item in jsonObj:
                result['row ' + str(i)] = item
                i += 1
            return json.dumps(result, indent=4)

    def writeTurtleFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            f = open(self.getFilePathToWriteTurtle(), "w")
            g = Graph().parse(data=str(json.dumps(jsonObj, indent=4)), format='json-ld')
            f.write(g.serialize(format='n3'))
            # print(g.serialize(format='n3'))
            f.close()

        # for when we have multiple files to be annotated, mainly for CSV files
        else:
            i = 1
            for item in jsonObj:
                f = open(re.sub("[.]", '_'+str(i)+'.', self.getFilePathToWriteTurtle()), "w")
                g = Graph().parse(data=str(json.dumps(item, indent=4)), format='json-ld')
                f.write(g.serialize(format='n3'))
                i += 1
                f.close()

    # returns a turtle formatted result for the API
    def getTurtleFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            g = Graph().parse(data=str(json.dumps(jsonObj, indent=4)), format='json-ld')
            return g.serialize(format='n3')

        # for when we have multiple files to be annotated, mainly for CSV files
        else:
            result = {}
            i = 1
            for item in jsonObj:
                g = Graph().parse(data=str(json.dumps(item, indent=4)), format='json-ld')
                result['row ' + str(i)] = g.serialize(format='n3').strip()
                i += 1

            return result

    def writeOWLFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            f = open(self.getFilePathToWriteOWL(), "w")
            g = Graph().parse(data=str(json.dumps(jsonObj, indent=4)), format='json-ld')
            f.write(g.serialize(format='pretty-xml'))
            f.close()

        # for when we have multiple files to be annotated, mainly for CSV files
        else:
            i = 1
            for item in jsonObj:
                f = open(re.sub("[.]", '_'+str(i)+'.', self.getFilePathToWriteOWL()), "w")
                g = Graph().parse(data=str(json.dumps(item, indent=4)), format='json-ld')
                f.write(g.serialize(format='pretty-xml'))
                i += 1
                f.close()

    # returns a owl formatted result for the API
    def getOWLFile(self, jsonObj):
        if isinstance(jsonObj, dict):
            g = Graph().parse(data=str(json.dumps(jsonObj, indent=4)), format='json-ld')
            return g.serialize(format='pretty-xml')

        # for when we have multiple files to be annotated, mainly for CSV files
        else:
            result = {}
            i = 1
            for item in jsonObj:
                g = Graph().parse(data=str(json.dumps(item, indent=4)), format='json-ld')
                result['row' + str(i)] = g.serialize(format='pretty-xml')
                i += 1
            return result
