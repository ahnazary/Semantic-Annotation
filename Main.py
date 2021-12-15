import time

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector
from SecondLayer import SecondLayer

start_time = time.time()
filenameJSON = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
fileNameOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl"

readJSON = ReadJSON(filenameJSON)
featureVector = FeatureVector(readJSON.getAllKeywords(), fileNameOntology)
featureVector.getClassNode("http://webprotege.stanford.edu/refBuilding")
# print(featureVector.isClassNode("http://webprotege.stanford.edu/Convertor"))
featureVector.test()


# firstLayer = FirstLayer(readJSON.getAllKeywords(), fileNameOntology)
# firstLayer.generateFirstLayerResultList()

secondLayer = SecondLayer(readJSON.getAllKeywords(), fileNameOntology)
secondLayer.generateSecondLayerResultList()
print(FeatureVector.getQueryURIs())
print(len(FeatureVector.getQueryURIs()))

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))