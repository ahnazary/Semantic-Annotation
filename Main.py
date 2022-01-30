import os
import time
import glob

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON

from FeatureVector import FeatureVector, queryURIs, queryURIsTuples, finalURIs
from SecondLayer import SecondLayer
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec
from JSONLDGenerator import JSONLDGenerator

start_time = time.time()

SQLDatabase.readPDFSIntoSQLTable()
myThing = MyWord2Vec()
MyWord2Vec.startTokenizingInputText(SQLDatabase.readPDFContentsIntoASingleString())

projectPath = os.path.abspath(os.path.dirname(__file__))
path = projectPath + "/files/*.json"
print("path uis ", path)

for file in glob.glob(path):
    SQLDatabase.removeDuplicateRows()
    print(file)
    filePathJSON = str(file)
    filePathOntology = projectPath + "/files/saref.ttl"

    readJSON = ReadJSON(filePathJSON)

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()

    featureVector = FeatureVector(readJSON.getAllKeywords(), filePathOntology)

    firstLayer = FirstLayer(readJSON.getAllKeywords(), filePathOntology)
    firstLayer.generateFirstLayerResultList()

    secondLayer = SecondLayer(readJSON.getAllKeywords(), filePathOntology)
    secondLayer.generateSecondLayerResultList()
    featureVector.setPopularityFeatures()

    for item in featureVector.getqueryURIsTuples():
        print(item, featureVector.getqueryURIsTuples()[item])

    featureVector.generateFinalURIs()

    JSONLD = JSONLDGenerator(file, finalURIs)

    print("size of query uris is :", len(queryURIs))
    print("most frequent URI is : ", queryURIs.count(featureVector.most_frequent(queryURIs)))

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    finalURIs.clear()
    readJSON.keywords.clear()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
