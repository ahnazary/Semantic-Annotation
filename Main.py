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
featureVector.test()
# featureVector.getClassNode("https://w3id.org/saref#SensingFunction")
# print(featureVector.isClassNode(":makesMeasurement"))
# print(featureVector.getPrefName("http://webprotege.stanford.edu/Compressor"))

# firstLayer = FirstLayer(readJSON.getAllKeywords(), fileNameOntology)
# firstLayer.generateFirstLayerResultList()
#
# secondLayer = SecondLayer(readJSON.getAllKeywords(), fileNameOntology)
# secondLayer.generateSecondLayerResultList()

print("Result list is : ")
for uri in featureVector.getQueryURIs():
    print("    ",uri)

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))