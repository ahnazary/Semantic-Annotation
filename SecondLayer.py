from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples
from URIsDatabase import URIsDatabase
from termcolor import colored


class SecondLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl":
            self.ontologyStr = "SAREF"

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateSecondLayerResultList(self):
        global flag, word
        layer = "secondLayer"
        database = URIsDatabase()
        for word in self.keywords:
            flag = True
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            print(word, "2nd")
            if URIsDatabase.keywordExists(word, self.ontologyStr, layer):
                URIsDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer)
            if not URIsDatabase.keywordExists(word, self.ontologyStr, layer):
                queryStrExact = prefixes + """SELECT ?subject
                   WHERE{
                   {?subject ?a ?object} UNION{
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

                        database.addToURIsParents(URI, isParent, None)
                        database.addToKeywords(word, self.ontologyStr, layer, URI)
                        flag = False
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

                        database.addToURIsParents(URI, isParent, parents)
                        if parents != "Has no parent":
                            database.addToKeywords(word, self.ontologyStr, layer, parents)
                            flag = False
                if flag:
                    database.addToKeywords(word, self.ontologyStr, layer, None)
                    str = 'No URI found for: ' + word + " in the Ontology"
                    print(colored(str, 'magenta'))

        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            print(word, "2nd")
            if URIsDatabase.keywordExists(word, self.ontologyStr, layer):
                URIsDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer)
            if not URIsDatabase.keywordExists(word, self.ontologyStr, layer):
                for i in range(0, len(word) + 1, 1):
                    for j in range(i + 3, len(word) + 1, 1):
                        subString = word[i:j]
                        if subString in bannedStrings or len(subString) <= 2:
                            continue
                        print(subString, "2nd")
                        queryStr = prefixes + """SELECT ?subject
                            WHERE{
                            {?subject ?a ?object} UNION{
                            ?subject rdfs:label ?object}
                             FILTER (regex(?object, \" """ + subString + " \", \"i\" ))}"

                        queryResult = self.ontology.query(queryStr)
                        for row in queryResult:
                            URI = f"{row.subject}"
                            isParent = FeatureVector.isClassNode(self, URI)
                            if isParent and URI not in bannedURIs:
                                print(URI, isParent)
                                queryURIs.append(URI)

                                similarity = float("{:.4f}".format(len(subString) / len(word)))
                                tempTuple = (similarity, 2)
                                if URI in queryURIsTuples:
                                    if queryURIsTuples[URI][1] < 2 and queryURIsTuples[URI][0] > similarity:
                                        queryURIsTuples[URI] = tempTuple
                                else:
                                    queryURIsTuples[URI] = tempTuple

                                database.addToURIsParents(URI, isParent, None)
                                database.addToKeywords(word, self.ontologyStr, layer, URI)
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
                                        if queryURIsTuples[uri][1] < 2 and queryURIsTuples[uri][0] > similarity:
                                            queryURIsTuples[uri] = tempTuple
                                    else:
                                        queryURIsTuples[URI] = tempTuple
                                database.addToURIsParents(URI, isParent, parents)
                                database.addToKeywords(word, self.ontologyStr, layer, parents)

            if flag:
                database.addToKeywords(word, self.ontologyStr, layer, None)
                str = 'No URI found for: ' + word + " in the Ontology"
                print(colored(str, 'magenta'))
