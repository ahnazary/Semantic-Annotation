import time

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector

start_time = time.time()
filenameJSON = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
filenameOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl"

readJSON = ReadJSON(filenameJSON)
featureVector = FeatureVector(readJSON.getAllKeywords(), filenameOntology)

firstLayer = FirstLayer(readJSON.getAllKeywords(), filenameOntology)
firstLayer.generateFirstLayerResultList()
print(featureVector.getQueryURIs())

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
