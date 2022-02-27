import json
import os
import re

from termcolor import colored

from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples, finalJson, \
    finalContext
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology, fileJsonObject):
        super().__init__(keywords, ontology, fileJsonObject)
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if ontology == projectPath + "/AllFiles/Sargon.ttl":
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
        for key, value in self.fileJsonObject.items():
            if bool(re.match('^.?id$', key)) or bool(re.match('^.?type$', key)):
                pass
            elif isinstance(value, str) or isinstance(value, list):
                finalJson[key] = {"value": value}
                finalContext[key] = self.getRelatedNode(key)

        finalJson["context"] = finalContext
        print(json.dumps(finalJson, indent=4))

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
                result = SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer, tempUse='yes')
                tempQueryURIsTuples[result[0]] = (result[1], result[2])
                return tempQueryURIsTuples
            elif not SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                for i in range(0, len(word) + 1, 1):
                    for j in range(i + 3, len(word) + 1, 1):
                        subString = word[i:j].lower()
                        if subString in bannedStrings or len(subString) <= 2:
                            continue
                        queryStr = prefixes + """SELECT ?subject
                            WHERE{
                            ?subject rdfs:comment ?object.
                            FILTER regex(str(?object), \"[^a-zA-Z]+""" + subString.lower() + "[^a-zA-Z]+\", \"i\")}"

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
                return tempQueryURIsTuples
                # queryStrExact = prefixes + """SELECT ?subject
                #                    WHERE{
                #                    {?subject ?a ?object} UNION{
                #                    ?subject rdfs:label ?object}
                #                    FILTER regex(?object, \"""" + word + "\", \"i\" )}"
                # queryResult = self.ontology.query(queryStrExact)
                # for row in queryResult:
                #     URI = f"{row.subject}"
                #     isParent = self.isClassNode(URI)
                #     if isParent and URI not in bannedURIs:
                #         cbow = MyWord2Vec.GetCBOW(word, URI)
                #         skipgram = MyWord2Vec.GetSkipGram(word, URI)
                #         tempQueryURIs.append(URI)
                #         if URI in tempQueryURIsTuples:
                #             if tempQueryURIsTuples[URI][1] > cbow:
                #                 tempQueryURIsTuples[URI] = (cbow, skipgram)
                #         else:
                #             tempQueryURIsTuples[URI] = (cbow, skipgram)
                #         database.addToURIsParents(URI, isParent, None)
                #         database.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipgram)
                #         flag = False
                #
                #     if not isParent and URI not in bannedURIs:
                #         parents = self.getClassNode(URI)
                #         if len(self.getClassNode(URI)) == 0:
                #             parents = ["Has no parent"]
                #         else:
                #             for uri in parents:
                #                 cbow = MyWord2Vec.GetCBOW(word, uri)
                #                 skipgram = MyWord2Vec.GetSkipGram(word, uri)
                #                 queryURIs.append(uri)
                #                 database.addToKeywords(word, self.ontologyStr, layer, uri, cbow, skipgram)
                #                 database.addToURIsParents(URI, isParent, uri)
                #                 flag = False
                #                 if uri in queryURIsTuples:
                #                     if queryURIsTuples[uri][1] > cbow:
                #                         queryURIsTuples[uri] = (cbow, skipgram)
                #                 else:
                #                     queryURIsTuples[uri] = (cbow, skipgram)

            # if no URI found for the keyword
            if flag:
                database.addToKeywords(word, self.ontologyStr, layer, None, None, None)
                str = 'No URI found for: ' + word + " in the Ontology"
                # print(colored(str, 'magenta'))