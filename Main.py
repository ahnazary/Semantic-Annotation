import os
import time
import glob

from FirstLayer import FirstLayer
from ExtractKeywords import ExtractKeywords

from FeatureVector import FeatureVector, queryURIs, queryURIsTuples, finalURIs, finalContext
from SecondLayer import SecondLayer
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
    filePath = str(file)
    filePathOntology = projectPath + "/AllFiles/saref.ttl"

    extractKeywords = ExtractKeywords(filePath)

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()

    allKeywords = extractKeywords.getAllKeywords()[0]
    fileJsonObject = extractKeywords.getAllKeywords()[1]
    featureVector = FeatureVector(allKeywords, filePathOntology, fileJsonObject)

    firstLayer = FirstLayer(allKeywords, filePathOntology, fileJsonObject)
    firstLayer.generateFirstLayerResultList()
    firstLayer.buildFinalJson()

    secondLayer = SecondLayer(allKeywords, filePathOntology, fileJsonObject)
    secondLayer.generateSecondLayerResultList()
    featureVector.setPopularityFeatures()

    for item in featureVector.getQueryURIsTuples():
        print(item, featureVector.getQueryURIsTuples()[item])

    featureVector.generateFinalURIs()

    outputGenerator = OutputGenerator(file, finalURIs)
    outputGenerator.WriteJSONLDFile()

    print("size of query uris is :", len(queryURIs))
    print("most frequent URI is : {} with {} repetitions".format(featureVector.most_frequent(queryURIs),
                                                                 queryURIs.count(
                                                                     featureVector.most_frequent(queryURIs))))

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    finalURIs.clear()
    extractKeywords.keywords.clear()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
