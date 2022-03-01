import json
import os
import re

from termcolor import colored

from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples, finalJson, \
    finalContext
from OutputGenerator import OutputGenerator
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology, fileJsonObject):
        super().__init__(keywords, ontology, fileJsonObject)
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if ontology == projectPath + "/AllFiles/sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == projectPath + "/AllFiles/saref.ttl":
            self.ontologyStr = "SAREF"

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateFirstLayerResultList(self):
        layer = "firstLayer"
        for word in self.keywords:
            flag = True
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue

            if SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer)
            elif not SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                queryStrExact = prefixes + """SELECT ?subject
                    WHERE{
                    {?subject rdfs:label ?object}
                    FILTER (regex(?subject, \"""" + word + "\", \"i\" ) || contains(str(?subject), \'" + word + "\'))}"
                queryResult = self.ontology.query(queryStrExact)
                self.createFeatureVectorForQueryResult(queryResult, word, layer)

                # if no URI found for the keyword
                if flag:
                    SQLDatabase.addToKeywords(word, self.ontologyStr, layer, None, None, None)

    def createFeatureVectorForQueryResult(self, queryResult, word, layer):
        for row in queryResult:
            URI = f"{row.subject}"
            isParent = FeatureVector.isClassNode(self, URI)
            if isParent and URI not in bannedURIs:
                cbow = MyWord2Vec.GetCBOW(word, URI)
                skipgram = MyWord2Vec.GetSkipGram(word, URI)
                # print(URI, isParent)
                queryURIs.append(URI)
                queryURIsTuples[URI] = (cbow, skipgram)
                SQLDatabase.addToURIsParents(URI, isParent, None)
                SQLDatabase.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipgram)

            if not isParent and URI not in bannedURIs:
                cbow = MyWord2Vec.GetCBOW(word, URI)
                skipgram = MyWord2Vec.GetSkipGram(word, URI)
                parents = FeatureVector.getClassNode(self, URI)
                if len(parents) == 0:
                    parents = "Has no parent"
                for uri in parents:
                    queryURIs.append(uri)
                    queryURIsTuples[uri] = (cbow, skipgram)
                    SQLDatabase.addToURIsParents(URI, isParent, uri)
                    SQLDatabase.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipgram)

    def buildFinalJson(self):
        hasID = False
        finalJson["@context"] = finalContext
        print(self.fileJsonObject)
        for key, value in self.fileJsonObject.items():
            if bool(re.match('^.?id$', key)):
                finalJson['@id'] = value
                hasID = True
            elif bool(re.match('^.?type$', key)):
                finalJson['@type'] = value
            elif isinstance(value, str) or isinstance(value, list) or isinstance(value, int) or isinstance(value, bool):
                finalJson[key] = value
                finalContext[key] = self.getRelatedNode(key)

            # this need some work
            elif isinstance(value, dict):
                finalJson[key] = value['value']
                finalContext[key] = self.getRelatedNode(key)
        if not hasID and len(queryURIs) > 0:
            if self.isClassNode(self.most_frequent(queryURIs)):
                finalJson['@id'] = self.most_frequent(queryURIs)
            else:
                finalJson['@id'] = self.getClassNode(self.most_frequent(queryURIs))
        return finalJson

    def getRelatedNode(self, word):
        tempQueryURIs = []
        tempQueryURIsTuples = {}
        queryStrExact = prefixes + """SELECT ?subject
                WHERE{
                ?subject rdfs:label ?object.
                FILTER regex(str(?subject), \".*[/:@]""" + word.lower() + "$\", \"i\")}"
        queryResult = self.ontology.query(queryStrExact)

        if len(queryResult) == 1:
            for row in queryResult: return f"{row.subject}"
        else:
            layer = "secondLayer"
            database = SQLDatabase()
            flag = True
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                return None
            elif SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                tempQueryResult = SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer, tempUse='yes')
                if tempQueryResult is not False:
                    tempQueryURIsTuples = tempQueryResult
                print(tempQueryURIsTuples)
            elif not SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                for i in range(0, len(word) + 1, 1):
                    for j in range(i + 3, len(word) + 1, 1):
                        subString = word[i:j].lower()
                        if subString in bannedStrings or len(subString) <= 2:
                            continue
                        queryStr = prefixes + """SELECT ?subject
                            WHERE{
                            {
                            ?subject rdfs:comment ?object.
                            FILTER regex(str(?object), \"[^\\w]+""" + subString + """[^\\w]+\", \"i\")
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
                                tempQueryURIs.append(URI)
                                # similarity = float("{:.4f}".format(len(subString) / len(word)))
                                if URI in tempQueryURIsTuples:
                                    if tempQueryURIsTuples[URI][1] > cbow:
                                        tempQueryURIsTuples[URI] = (cbow, skipgram)
                                else:
                                    tempQueryURIsTuples[URI] = (cbow, skipgram)

                                database.addToURIsParents(URI, isParent, None)
                                database.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipgram)
                            if not isParent and URI not in bannedURIs:
                                parents = self.getClassNode(URI)
                                if len(parents) == 0:
                                    parents = ["Has no parent"]
                                for uri in parents:
                                    tempQueryURIs.append(uri)
                                    cbow = MyWord2Vec.GetCBOW(word, uri)
                                    skipgram = MyWord2Vec.GetSkipGram(word, uri)
                                    # similarity = float("{:.4f}".format(len(subString) / len(word)))
                                    database.addToKeywords(word, self.ontologyStr, layer, uri, cbow, skipgram)
                                    database.addToURIsParents(URI, isParent, uri)
                                    flag = False
                                    if uri in tempQueryURIsTuples:
                                        if tempQueryURIsTuples[uri][1] > cbow:
                                            tempQueryURIsTuples[uri] = (cbow, skipgram)
                                    else:
                                        tempQueryURIsTuples[URI] = (cbow, skipgram)
                print("hello", tempQueryURIsTuples)
                for key, value in tempQueryURIsTuples.items():
                    tempQueryURIsTuples[key] = pow(value[0], 2) + pow(value[1], 2)

            # if no URI found for the keyword
            if flag:
                database.addToKeywords(word, self.ontologyStr, layer, None, None, None)
        if len(tempQueryURIsTuples) >= 1:
            return max(tempQueryURIsTuples, key=tempQueryURIsTuples.get)
        else:
            return ""
