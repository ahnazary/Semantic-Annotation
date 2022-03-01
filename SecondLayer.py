import os

from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec


class SecondLayer(FeatureVector):
    def __init__(self, keywords, ontology, fileJsonObject):
        super().__init__(keywords, ontology, fileJsonObject)
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if ontology == projectPath + "/AllFiles/sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == projectPath + "/AllFiles/saref.ttl":
            self.ontologyStr = "SAREF"

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateSecondLayerResultList(self):
        layer = "secondLayer"
        database = SQLDatabase()
        for word in self.keywords:
            flag = True
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            # print(word, "2nd")
            elif SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer)
            elif not SQLDatabase.keywordExists(word, self.ontologyStr, layer):
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
                        cbow = MyWord2Vec.GetCBOW(word, URI)
                        skipgram = MyWord2Vec.GetSkipGram(word, URI)
                        queryURIs.append(URI)
                        if URI in queryURIsTuples:
                            if queryURIsTuples[URI][1] > cbow:
                                queryURIsTuples[URI] = (cbow, skipgram)
                        else:
                            queryURIsTuples[URI] = (cbow, skipgram)

                        database.addToURIsParents(URI, isParent, None)
                        database.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipgram)
                        flag = False

                    if not isParent and URI not in bannedURIs:
                        parents = FeatureVector.getClassNode(self, URI)
                        if len(FeatureVector.getClassNode(self, URI)) == 0:
                            parents = ["Has no parent"]
                        for uri in parents:
                            cbow = MyWord2Vec.GetCBOW(word, uri)
                            skipgram = MyWord2Vec.GetSkipGram(word, uri)
                            queryURIs.append(uri)
                            database.addToKeywords(word, self.ontologyStr, layer, uri, cbow, skipgram)
                            database.addToURIsParents(URI, isParent, uri)
                            flag = False
                            if uri in queryURIsTuples:
                                if queryURIsTuples[uri][1] > cbow:
                                    queryURIsTuples[uri] = (cbow, skipgram)
                            else:
                                queryURIsTuples[uri] = (cbow, skipgram)

                # if no URI found for the keyword
                if flag:
                    database.addToKeywords(word, self.ontologyStr, layer, None, None, None)

        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            # print(word, "2nd")
            if SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer)
            if not SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                for i in range(0, len(word) + 1, 1):
                    for j in range(i + 3, len(word) + 1, 1):
                        subString = word[i:j].lower()
                        if subString in bannedStrings or len(subString) <= 2:
                            continue
                        # print(subString, "2nd")
                        queryStr = prefixes + """SELECT ?subject
                            WHERE{
                            {
                            ?subject rdfs:comment ?object.
                            FILTER regex(str(?object), \"[^a-zA-Z]+""" + subString + """[^a-zA-Z]+\", \"i\")
                            }
                            UNION
                            {
                            ?subject rdfs:label ?object.
                            FILTER regex(str(?object), \"[^a-zA-Z]+""" + subString + """[^a-zA-Z]+\", \"i\")
                            }
                            UNION
                            {
                            ?subject rdfs:label ?object.
                            FILTER regex(str(?object), \"^""" + subString + """[^a-zA-Z]+\", \"i\")
                            }
                            UNION
                            {
                            ?subject rdfs:label ?object.
                            FILTER regex(str(?object), \"[^a-zA-Z]+""" + subString + """$\", \"i\")
                            }
                            UNION
                            {
                            ?subject rdfs:label ?object.
                            FILTER regex(str(?object), \"^""" + subString + """$\", \"i\")
                            }
                            }"""

                        queryResult = self.ontology.query(queryStr)
                        for row in queryResult:
                            URI = f"{row.subject}"
                            isParent = FeatureVector.isClassNode(self, URI)
                            if isParent and URI not in bannedURIs:
                                cbow = MyWord2Vec.GetCBOW(word, URI)
                                skipgram = MyWord2Vec.GetSkipGram(word, URI)
                                queryURIs.append(URI)
                                # similarity = float("{:.4f}".format(len(subString) / len(word)))
                                if URI in queryURIsTuples:
                                    if queryURIsTuples[URI][1] > cbow:
                                        queryURIsTuples[URI] = (cbow, skipgram)
                                else:
                                    queryURIsTuples[URI] = (cbow, skipgram)

                                database.addToURIsParents(URI, isParent, None)
                                database.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipgram)
                            if not isParent and URI not in bannedURIs:
                                parents = FeatureVector.getClassNode(self, URI)
                                if len(parents) == 0:
                                    parents = ["Has no parent"]
                                for uri in parents:
                                    queryURIs.append(uri)
                                    cbow = MyWord2Vec.GetCBOW(word, uri)
                                    skipgram = MyWord2Vec.GetSkipGram(word, uri)
                                    # similarity = float("{:.4f}".format(len(subString) / len(word)))
                                    database.addToKeywords(word, self.ontologyStr, layer, uri, cbow, skipgram)
                                    database.addToURIsParents(URI, isParent, uri)
                                    flag = False
                                    if uri in queryURIsTuples:
                                        if queryURIsTuples[uri][1] > cbow:
                                            queryURIsTuples[uri] = (cbow, skipgram)
                                    else:
                                        queryURIsTuples[URI] = (cbow, skipgram)

            # if no URI found for the keyword
            if flag:
                database.addToKeywords(word, self.ontologyStr, layer, None, None, None)

