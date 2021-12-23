import sqlite3
import time

from termcolor import colored

from FirstLayer import FirstLayer
from ReadJSON import ReadJSON
from FeatureVector import FeatureVector
from SecondLayer import SecondLayer
from URIsDatabase import URIsDatabase

start_time = time.time()
filePathJSON = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Room-example.json"
filePathOntology = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl"

readJSON = ReadJSON(filePathJSON)

URIsDatabase.createKeywordsTable()
URIsDatabase.createURIsParentsTable()

featureVector = FeatureVector(readJSON.getAllKeywords(), filePathOntology)

firstLayer = FirstLayer(readJSON.getAllKeywords(), filePathOntology)
firstLayer.generateFirstLayerResultList()

# secondLayer = SecondLayer(readJSON.getAllKeywords(), filePathOntology)
# secondLayer.generateSecondLayerResultList()

print(FeatureVector.getQueryURIs())
print(len(FeatureVector.getQueryURIs()))

featureVector.setPopularityFeatures()

URIs = featureVector.getqueryURIsTuples()
for item in URIs:
    print(item, URIs[item])

print(featureVector.most_frequent(FeatureVector.getQueryURIs()))
print(FeatureVector.getQueryURIs().count(featureVector.most_frequent(FeatureVector.getQueryURIs())))


conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()
sqlstr = 'SELECT keyword, URI FROM Keywords'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])
    print(row[1], type(row[1]))

cur.close()

URIsDatabase.removeDuplicateRows()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))