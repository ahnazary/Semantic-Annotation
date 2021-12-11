import time

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector
from SecondLayer import SecondLayer

start_time = time.time()
filenameJSON = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
filenameOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl"

readJSON = ReadJSON(filenameJSON)
featureVector = FeatureVector(readJSON.getAllKeywords(), filenameOntology)
# featureVector.getClassNode(":relatesToMeasurement")
# print(featureVector.isClassNode(":makesMeasurement"))
featureVector.getPrefName("https://w3id.org/saref#SensingFunction")

# firstLayer = FirstLayer(readJSON.getAllKeywords(), filenameOntology)
# firstLayer.generateFirstLayerResultList()
#
# secondLayer = SecondLayer(readJSON.getAllKeywords(), filenameOntology)
# secondLayer.generateSecondLayerResultList()

print("Result list is : ")
for uri in featureVector.getQueryURIs():
    print("    ",uri)

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
