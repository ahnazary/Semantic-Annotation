import time

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector
from SecondLayer import SecondLayer

start_time = time.time()
filePathJSON = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
filePathOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl"

readJSON = ReadJSON(filePathJSON)
featureVector = FeatureVector(readJSON.getAllKeywords(), filePathOntology)
# featureVector.getClassNode("http://webprotege.stanford.edu/refBuilding")
# print(featureVector.isClassNode("http://webprotege.stanford.edu/Convertor"))
# featureVector.test()
# print(featureVector.getStringOfList(featureVector.getBannedStrings()))

# firstLayer = FirstLayer(readJSON.getAllKeywords(), filePathOntology)
# firstLayer.generateFirstLayerResultList()
secondLayer = SecondLayer(readJSON.getAllKeywords(), filePathOntology)
secondLayer.generateSecondLayerResultList()

print(FeatureVector.getQueryURIs())
print(len(FeatureVector.getQueryURIs()))

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))