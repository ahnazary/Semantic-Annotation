import json
import rdflib

fh = open("/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Floor-example.json")
jsonData = json.load(fh)

keywords = list()


def jsonExtractor(input):
    for entry in input:
        # print(entry)
        keywords.append(entry)
        if isinstance(input[entry], str):
            keywords.append(input[entry])
        # print(input[entry], type(input[entry]))
        if isinstance(input[entry], list):
            for i in input[entry]:
                keywords.append(i)
        if isinstance(input[entry], dict):
            jsonExtractor(input[entry])


jsonExtractor(jsonData)

for i in keywords:
    print(i)

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