import json
import os
import re

from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples, finalJson, \
    finalContext
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

    def buildFinalJson(self):
        hasID = False
        finalJson["@context"] = finalContext
        for key, value in self.fileJsonObject.items():
            if bool(re.match('^.?id$', str(key))):
                finalJson['@id'] = value
                hasID = True
            elif bool(re.match('^.?type$', str(key))):
                finalJson['@type'] = value
            elif isinstance(value, str) or isinstance(value, list) or isinstance(value, int) or isinstance(value, bool):
                finalContext[key] = self.getRelatedNode(key)
                if self.isClassNode(finalContext[key]):
                    finalJson[key] = {"@type": "relationship", "@value": value}
                else:
                    finalJson[key] = {"@type": "property", "@value": value}

            # this need some work
            elif isinstance(value, dict):
                valueDict = {}
                for item in value:
                    if not bool(re.match('.*type?', str(item))) and not bool(re.match('.*value?', str(item))):
                        valueDict[item] = value[item]
                if 'value' in value and len(valueDict) == 0:
                    valueDict = value['value']
                elif 'value' in value and len(valueDict) != 0:
                    valueDict['value'] = value['value']
                finalContext[key] = self.getRelatedNode(key)
                if any(match for match in [re.match(".*type?",i) for i in value]):
                    tempType = value[[re.findall(".*type?", j) for j in value][0][0]]
                    finalJson[key] = {"@type": tempType}
                    if self.isClassNode(finalContext[key]):
                        finalJson[key]['@value'] = valueDict
                    else:
                        finalJson[key]['@value'] = valueDict
                else:
                    if self.isClassNode(finalContext[key]):
                        finalJson[key] = {"@type": "Relationship", "@value": value['value']}
                    else:
                        finalJson[key] = {"@type": "Property", "@value": value['value']}

        if not hasID:
            secondLayer = SecondLayer(self.keywords, self.ontologyFilePath, self.fileJsonObject)
            secondLayer.generateSecondLayerResultList()
            self.featureVector.setPopularityFeatures()
            for item in self.featureVector.getQueryURIsTuples():
                print(item, self.featureVector.getQueryURIsTuples()[item])
            self.featureVector.generateFinalURIs()
            print("size of query uris is :", len(queryURIs))
            print("most frequent URI is : {} with {} repetitions".format(self.featureVector.most_frequent(queryURIs),
                                                                         queryURIs.count(
                                                                             self.featureVector.most_frequent(
                                                                                 queryURIs))))
            if len(queryURIs) > 0:
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
