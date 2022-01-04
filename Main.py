import time
import glob

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON

from FeatureVector import FeatureVector, queryURIs, queryURIsTuples
from SecondLayer import SecondLayer
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec
from JSONLDGenerator import JSONLDGenerator

start_time = time.time()


SQLDatabase.readPDFSIntoSQLTable()
myThing = MyWord2Vec()
MyWord2Vec.startTokenizingInputText(SQLDatabase.readPDFContentsIntoASingleString())

# print("final is ", MyWord2Vec.GetCBOW("Sensor", "https://saref.etsi.org/core/Profile"))
# print("final is ", MyWord2Vec.GetSkipGram("actuator", "https://saref.etsi.org/core/Actuator"))


for file in glob.glob("/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/*.json"):
    SQLDatabase.removeDuplicateRows()
    print(file)
    filePathJSON = str(file)
    filePathOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl"

    readJSON = ReadJSON(filePathJSON)

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()

    featureVector = FeatureVector(readJSON.getAllKeywords(), filePathOntology)

    firstLayer = FirstLayer(readJSON.getAllKeywords(), filePathOntology)
    firstLayer.generateFirstLayerResultList()

    secondLayer = SecondLayer(readJSON.getAllKeywords(), filePathOntology)
    secondLayer.generateSecondLayerResultList()

    featureVector.setPopularityFeatures()

    for i in queryURIsTuples:
        print(i)
        print("size of query uris is :", len(queryURIs))
    print("most frequent URI is : ", queryURIs.count(featureVector.most_frequent(queryURIs)))

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    readJSON.keywords.clear()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
