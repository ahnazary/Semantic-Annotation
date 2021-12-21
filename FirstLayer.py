from CreateSQL import CreateSQL
from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples
from KeywordsSQL import KeywordsSQL


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl":
            self.ontologyStr = "SAREF"

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateFirstLayerResultList(self):
        createSQl = CreateSQL()
        keywordsSQL = KeywordsSQL()
        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() or not i == ":"])
            print(word, "1st")
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            queryStrExact = prefixes + """SELECT ?subject
                WHERE{
                {?subject rdfs:label ?object}
                FILTER (regex(?object, \"""" + word + "\", \"i\" ) || contains(str(?subject), \'" + word + "\'))}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                URI = f"{row.subject}"
                isParent = FeatureVector.isClassNode(self, URI)
                if isParent and URI not in bannedURIs:
                    print(URI, isParent)
                    queryURIs.append(URI)
                    tempTuple = (1, 1)
                    queryURIsTuples[URI] = tempTuple

                    createSQl.addURI(URI, isParent, None)
                    keywordsSQL.addKeyword(word, self.ontologyStr, URI)

                if not isParent and URI not in bannedURIs:
                    print(URI, isParent)
                    print("   ", FeatureVector.getClassNode(self, URI))
                    parents = FeatureVector.getStringOfList(FeatureVector.getClassNode(self, URI))
                    if len(parents) == 0:
                        parents = "Has no parent"
                    for uri in FeatureVector.getClassNode(self, URI):
                        queryURIs.append(uri)
                        tempTuple = (1, 1)
                        queryURIsTuples[uri] = tempTuple

                    createSQl.addURI(URI, isParent, parents)
                    keywordsSQL.addKeyword(word, self.ontologyStr, parents)
