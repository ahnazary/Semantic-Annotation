from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs
from CreateSQL import CreateSQL


class SecondLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateSecondLayerResultList(self):
        createSQl = CreateSQL()
        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            print(word, "1st")

            queryStrExact = prefixes + """SELECT ?subject
               WHERE{
               {?subject rdfs:comment ?object} UNION{
               ?subject rdfs:label ?object}
               FILTER regex(?object, \"""" + word + "\", \"i\" )}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                URI = f"{row.subject}"
                isParent = FeatureVector.isClassNode(self, URI)
                if isParent and URI not in bannedURIs:
                    # print(URI, isParent)
                    queryURIs.append(URI)
                    createSQl.addURI(URI, isParent, None)
                if not isParent and URI not in bannedURIs:
                    print(URI, isParent)
                    print("   ", FeatureVector.getClassNode(self, URI))
                    parents = FeatureVector.getStringOfList(FeatureVector.getClassNode(self, URI))
                    if len(parents) == 0:
                        parents = "Has no parent"
                    createSQl.addURI(URI, isParent, parents)

        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            for i in range(0, len(word) + 1, 1):
                for j in range(i + 3, len(word) + 1, 1):
                    subString = word[i:j]
                    if subString in bannedStrings or len(subString) <= 2:
                        continue
                    print(subString, "2nd")
                    queryStr = prefixes + """SELECT ?subject
                        WHERE{
                        {?subject rdfs:comment ?object} UNION{
                        ?subject rdfs:label ?object}
                         FILTER (regex(?object, \" """ + subString + " \", \"i\" ))}"

                    queryResult = self.ontology.query(queryStr)
                    for row in queryResult:
                        URI = f"{row.subject}"
                        isParent = FeatureVector.isClassNode(self, URI)
                        if isParent and URI not in bannedURIs:
                            print(URI, isParent)
                            queryURIs.append(URI)
                        if not isParent and URI not in bannedURIs:
                            print(f"{row.subject} ", isParent)
                            print("   ", FeatureVector.getClassNode(self, URI))

