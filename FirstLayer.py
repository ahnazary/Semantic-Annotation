import json
import os
import re

from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec
from SecondLayer import SecondLayer


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology, fileJsonObject):
        super().__init__(keywords, ontology, fileJsonObject)
        self.ontologyFilePath = ontology
        projectPath = os.path.abspath(os.path.dirname(__file__))
        if ontology == projectPath + "/AllFiles/sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == projectPath + "/AllFiles/saref.ttl":
            self.ontologyStr = "SAREF"

        self.featureVector = FeatureVector(keywords, ontology, fileJsonObject)

        # this dictionary saves final context fo generating JSON-LD
        self.finalContext = {}

    def buildFinalJson(self, *args):
        finalJsonld = {"@context": self.finalContext}

        if len(args) == 0:
            tempDict = self.fileJsonObject
        else:
            tempDict = args[0]

        # in case one single json Object is given
        if isinstance(tempDict, dict):
            hasType = False
            hasId = False

            for key, value in tempDict.items():
                if isinstance(value, dict):
                    finalJsonld[key] = self.constructValidJsonObjectForKey(key, value)
                elif not isinstance(value, dict):

                    # searching fro value, id and type in input json object
                    if bool(re.match('^.{0,2}id$', str(key))):
                        finalJsonld['@id'] = value
                        hasId = True
                    elif bool(re.match('^.{0,2}type$', str(key))):
                        finalJsonld['@type'] = value
                    elif bool(re.match('^.{0,2}value$', str(key))):
                        finalJsonld["@value"] = value
                    else:
                        relatedNode = self.getRelatedNode(key)
                        if relatedNode != "" and relatedNode is not None:
                            self.finalContext[key] = relatedNode
                            finalJsonld[key] = self.constructDictForBothStringPair(key, value)
                        else:
                            finalJsonld[key] = value

            # adding @type to main json body if it doesn't have id already
            if not hasType:
                relatedNode = self.getRelatedNode(self.keywords[1])
                if relatedNode is not None and relatedNode != "":
                    finalJsonld = self.prependPairIntoDict("@type", self.getRelatedNode(self.keywords[1]), finalJsonld)
                else:
                    finalJsonld = self.prependPairIntoDict("@type", self.getRelatedNode(self.keywords[0]), finalJsonld)

            # adding @id to main json body if it doesn't have id already
            if not hasId:
                finalJsonld = self.prependPairIntoDict("@id", self.keywords[1], finalJsonld)

            return finalJsonld

        # in case input is a CSV file and multiple Json Objects in a list are given as the input
        if isinstance(self.fileJsonObject, list):
            finalJsonldList = []
            for item in self.fileJsonObject:
                finalJsonldList.append(self.buildFinalJson(item))
            return finalJsonldList

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
            word = FeatureVector.removeDigitsFromString(word)
            if word.lower() in bannedStrings or len(word) <= 1:
                return None
            elif SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                tempQueryResult = SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer, tempUse='yes')
                if tempQueryResult is not False:
                    tempQueryURIsTuples = tempQueryResult
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
                                skipGram = MyWord2Vec.GetSkipGram(word, URI)
                                tempQueryURIs.append(URI)
                                # similarity = float("{:.4f}".format(len(subString) / len(word)))
                                if URI in tempQueryURIsTuples:
                                    if tempQueryURIsTuples[URI][1] > cbow:
                                        tempQueryURIsTuples[URI] = (cbow, skipGram)
                                else:
                                    tempQueryURIsTuples[URI] = (cbow, skipGram)

                                database.addToURIsParents(URI, isParent, None)
                                database.addToKeywords(word, self.ontologyStr, layer, URI, cbow, skipGram)
                            if not isParent and URI not in bannedURIs:
                                parents = self.getClassNode(URI)
                                if len(parents) == 0:
                                    parents = ""
                                for uri in parents:
                                    tempQueryURIs.append(uri)
                                    cbow = MyWord2Vec.GetCBOW(word, uri)
                                    skipGram = MyWord2Vec.GetSkipGram(word, uri)
                                    database.addToKeywords(word, self.ontologyStr, layer, uri, cbow, skipGram)
                                    # database.addToURIsParents(URI, isParent, parents)
                                    flag = False
                                    if uri in tempQueryURIsTuples:
                                        if tempQueryURIsTuples[uri][1] > cbow:
                                            tempQueryURIsTuples[uri] = (cbow, skipGram)
                                    else:
                                        tempQueryURIsTuples[URI] = (cbow, skipGram)
                for key, value in tempQueryURIsTuples.items():
                    tempQueryURIsTuples[key] = pow(value[0], 2) + pow(value[1], 2)

            # if no URI found for the keyword
            if flag:
                database.addToKeywords(word, self.ontologyStr, layer, None, None, None)
        if len(tempQueryURIsTuples) >= 1:
            return max(tempQueryURIsTuples, key=tempQueryURIsTuples.get)
        else:
            return ""

    def constructValidJsonObjectForKey(self, inputKey, inputValueDict):
        resultDict = {}
        valueDict = {}
        hasType = False
        needsValue = False
        if not bool(re.match('^.{0,2}id$', str(inputKey))) and not bool(re.match('^.{0,2}value$', str(inputKey))) and not bool(re.match('^.{0,2}type$', str(inputKey))):
            self.finalContext[inputKey] = self. getRelatedNode(inputKey)
        for key, value in inputValueDict.items():
            if isinstance(key, int) or isinstance(key, float):
                continue

            # remove digits from key
            key = FeatureVector.removeDigitsFromString(key)

            # searching fro value, id and type in input json object
            if bool(re.match('^.{0,2}id$', str(key))):
                resultDict['@id'] = value
            elif bool(re.match('^.{0,2}type$', str(key))):
                resultDict['@type'] = value
                hasType = True
            elif bool(re.match('^.{0,2}value$', str(key))):
                resultDict['@value'] = value
            elif self.getRelatedNode(key) == "" or self.getRelatedNode(key) is None:
                valueDict[key] = value
                needsValue = True

            elif not isinstance(value, dict):
                self.finalContext[key] = self.getRelatedNode(key)

                if self.isClassNode(self.finalContext[key]):
                    resultDict[key] = {"@type": self.getRelatedNode(key), "@value": value }
                else:
                    resultDict[key] = {"@type": self.getRelatedNode(key), "@value": value }

            # if value is of type dict
            elif isinstance(value, dict):
                resultDict[key] = self.constructValidJsonObjectForKey(key, value)

        if not hasType:
            resultDict['@type'] = self.getRelatedNode(inputKey)
        if needsValue:
            if '@value' in resultDict:
                valueDict['value'] = resultDict['@value']
                resultDict['@value'] = valueDict
            else:
                resultDict['@value'] = valueDict
        return resultDict

    def constructDictForBothStringPair(self, key, value):
        resultDict = {'@id': key, '@value': value, '@type': self.getRelatedNode(key)}
        return resultDict

