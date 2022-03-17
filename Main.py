import json
import os
import time
import glob

from FirstLayer import FirstLayer
from ExtractKeywords import ExtractKeywords

from FeatureVector import queryURIs, queryURIsTuples, finalURIs, FeatureVector
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
    allKeywords = extractKeywords.getAllKeywords()[0]
    fileJsonObject = extractKeywords.getAllKeywords()[1]

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()

    firstLayer = FirstLayer(allKeywords, filePathOntology, fileJsonObject)

    outputGenerator = OutputGenerator(file, finalURIs)

    finalJsonObjects = firstLayer.buildFinalJson()
    outputGenerator.writeJSONLDFileFromDict(finalJsonObjects)
    outputGenerator.writeTurtleFile(finalJsonObjects)
    outputGenerator.writeOWLFile(finalJsonObjects)

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    finalURIs.clear()
    extractKeywords.keywords.clear()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))