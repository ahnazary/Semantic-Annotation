import json
import os
import time
import glob

from FirstLayer import FirstLayer, finalJson
from ExtractKeywords import ExtractKeywords

from FeatureVector import queryURIs, queryURIsTuples, finalURIs, finalContext
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec
from OutputGenerator import OutputGenerator

start_time = time.time()

SQLDatabase.readPDFSIntoSQLTable()
myThing = MyWord2Vec()
MyWord2Vec.startTokenizingInputText(SQLDatabase.readPDFContentsIntoASingleString())

projectPath = os.path.abspath(os.path.dirname(__file__))
path = projectPath + "/files/*"

for file in glob.glob(path):
    SQLDatabase.removeDuplicateRows()
    print('\n', file)
    filePath = file
    filePathOntology = projectPath + "/AllFiles/sargon.ttl"

    extractKeywords = ExtractKeywords(filePath)

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()

    allKeywords = extractKeywords.getAllKeywords()[0]
    fileJsonObject = extractKeywords.getAllKeywords()[1]
    firstLayer = FirstLayer(allKeywords, filePathOntology, fileJsonObject)

    outputGenerator = OutputGenerator(file, finalURIs)
    outputGenerator.writeJSONLDFileFromDict(firstLayer.buildFinalJson())
    outputGenerator.writeTurtleFile(str(json.dumps(finalJson, indent=4)))
    outputGenerator.writeOWLFile(str(json.dumps(finalJson, indent=4)))

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    finalURIs.clear()
    extractKeywords.keywords.clear()
    finalJson.clear()
    finalContext.clear()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
