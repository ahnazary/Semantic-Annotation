import time

from CreateSQL import CreateSQL
from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector
from SecondLayer import SecondLayer

start_time = time.time()
filePathJSON = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
filePathOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl"

readJSON = ReadJSON(filePathJSON)

createSQL = CreateSQL()
createSQL.createTable()

featureVector = FeatureVector(readJSON.getAllKeywords(), filePathOntology)

firstLayer = FirstLayer(readJSON.getAllKeywords(), filePathOntology)
firstLayer.generateFirstLayerResultList()
secondLayer = SecondLayer(readJSON.getAllKeywords(), filePathOntology)
secondLayer.generateSecondLayerResultList()

print(FeatureVector.getQueryURIs())
print(len(FeatureVector.getQueryURIs()))

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))