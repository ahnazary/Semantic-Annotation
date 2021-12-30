import time
import glob

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector, queryURIs, queryURIsTuples
from SecondLayer import SecondLayer
from URIsDatabase import URIsDatabase

start_time = time.time()

for file in glob.glob("/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/*.json"):
    URIsDatabase.removeDuplicateRows()
    print(file)
    filePathJSON = str(file)
    filePathOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl"

    readJSON = ReadJSON(filePathJSON)

    URIsDatabase.createKeywordsTable()
    URIsDatabase.createURIsParentsTable()

    featureVector = FeatureVector(readJSON.getAllKeywords(), filePathOntology)

    firstLayer = FirstLayer(readJSON.getAllKeywords(), filePathOntology)
    firstLayer.generateFirstLayerResultList()

    secondLayer = SecondLayer(readJSON.getAllKeywords(), filePathOntology)
    secondLayer.generateSecondLayerResultList()


    # print(FeatureVector.getQueryURIs())
    # print(len(FeatureVector.getQueryURIs()))

    featureVector.setPopularityFeatures()

    for item in featureVector.getqueryURIsTuples():
        print(item, featureVector.getqueryURIsTuples()[item])

    print("size of query uris is :" , len(queryURIs))
    for i in queryURIs:
        print(i)
    print(queryURIs.count(featureVector.most_frequent(queryURIs)))

    URIsDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    readJSON.keywords.clear()

    print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
