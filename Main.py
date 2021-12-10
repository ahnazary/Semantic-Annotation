import time

from ReadJSON import ReadJSON
from FeatureVector import FeatureVector

start_time = time.time()
filename = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
r1 = ReadJSON(filename)
print(r1.getAllKeywords())

filename = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl"
fv = FeatureVector(r1.getAllKeywords(), filename)
fv.firstLayerQuery()
fv.secondLayerQuery()


print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
