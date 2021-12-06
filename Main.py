import rdflib

from ReadJSON import ReadJSON

filename = "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json"
r1 = ReadJSON(filename)
print(r1.getAllKeywords())

g = rdflib.Graph()
g.parse("/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl")

knows_query = """
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

SELECT ?a 
WHERE {
    ?a rdfs:subClassOf ?b
}"""

qres = g.query(knows_query)
for row in qres:
    print(row)
