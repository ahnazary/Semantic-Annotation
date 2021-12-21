from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples
from CreateSQL import CreateSQL
from KeywordsSQL import KeywordsSQL


class SecondLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl":
            self.ontologyStr = "SAREF"

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateSecondLayerResultList(self):
        createSQl = CreateSQL()
        keywordsSQL = KeywordsSQL()
        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            print(word, "2nd")

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
                    print(URI, isParent)
                    queryURIs.append(URI)
                    tempTuple = (1, 2)
                    if URI in queryURIsTuples:
                        if queryURIsTuples[URI][1] < 2:
                            queryURIsTuples[URI] = tempTuple
                    else:
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
                        tempTuple = (1, 2)
                        if uri in queryURIsTuples:
                            if queryURIsTuples[uri][1] < 2:
                                queryURIsTuples[uri] = tempTuple
                        else:
                            queryURIsTuples[uri] = tempTuple

                    createSQl.addURI(URI, isParent, parents)
                    if parents is not "Has no parent":
                        keywordsSQL.addKeyword(word, self.ontologyStr, parents)

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

                            similarity = float("{:.4f}".format(len(subString)/len(word)))
                            tempTuple = (similarity, 2)
                            if URI in queryURIsTuples:
                                if queryURIsTuples[URI][1] < 2 and queryURIsTuples[URI][2] > similarity:
                                    queryURIsTuples[URI] = tempTuple
                            else:
                                queryURIsTuples[URI] = tempTuple

                            createSQl.addURI(URI, isParent, None)
                            keywordsSQL.addKeyword(word, self.ontologyStr, URI)
                        if not isParent and URI not in bannedURIs:
                            print(f"{row.subject} ", isParent)
                            print("   ", FeatureVector.getClassNode(self, URI))
                            parents = FeatureVector.getStringOfList(FeatureVector.getClassNode(self, URI))
                            if len(parents) == 0:
                                parents = "Has no parent"
                            for uri in FeatureVector.getClassNode(self, URI):
                                queryURIs.append(uri)
                                similarity = float("{:.4f}".format(len(subString) / len(word)))
                                tempTuple = (similarity, 2)
                                if uri in queryURIsTuples:
                                    if queryURIsTuples[uri][1] < 2 and queryURIsTuples[uri][2] > similarity:
                                        queryURIsTuples[uri] = tempTuple
                                else:
                                    queryURIsTuples[URI] = tempTuple
                            createSQl.addURI(URI, isParent, parents)
                            keywordsSQL.addKeyword(word, self.ontologyStr, parents)

