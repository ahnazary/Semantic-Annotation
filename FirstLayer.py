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
            for key, value in tempDict.items():
                if isinstance(value, dict):
                    finalJsonld[key] = self.constructValidJsonObjectForKey(key, value)
                elif not isinstance(value, dict):
                    if bool(re.match('^.{0,2}id$', str(key))):
                        finalJsonld['@id'] = value
                    elif bool(re.match('^.{0,2}type$', str(key))):
                        finalJsonld['@type'] = value
                    elif bool(re.match('^.{0,2}value$', str(key))):
                        finalJsonld["@value"] = value
                    else:
                        finalJsonld[key] = value
                        relatedNode = self.getRelatedNode(key)
                        if relatedNode != "" and relatedNode is not None:
                            self.finalContext[key] = relatedNode
            if not hasType:
                finalJsonld["@type"] = self.getRelatedNode(self.keywords[1])

            return finalJsonld

        # in case input is a CSV file and thus multiple Json Objects are generated
        if isinstance(self.fileJsonObject, list):
            finalJsonldList = []
            for item in self.fileJsonObject:
                finalJsonldList.append(self.buildFinalJson(item))
            return finalJsonldList


        # hasID = False
        # tempRelatedNodeDict = {}
        # finalJson["@context"] = finalContext
        # for key, value in self.fileJsonObject.items():
        #
        #     # remove digits from key
        #     key = FeatureVector.removeDigitsFromString(key/)
        #     if bool(re.match('^.?id$', str(key))):
        #         finalJson['@id'] = value
        #         hasID = True
        #     elif bool(re.match('^.?type$', str(key))):
        #         finalJson['@type'] = value
        #
        #     elif isinstance(value, str) or isinstance(value, list) or isinstance(value, int) or isinstance(value, bool):
        #         if key in tempRelatedNodeDict:
        #             finalContext[key] = tempRelatedNodeDict[key]
        #         elif key not in tempRelatedNodeDict:
        #             finalContext[key] = self.getRelatedNode(key)
        #             tempRelatedNodeDict[key] = self.getRelatedNode(key)
        #         if self.isClassNode(finalContext[key]):
        #             finalJson[key] = {"@type": "relationship", "@value": value, "@id": self.getRelatedNode(key)}
        #         else:
        #             finalJson[key] = {"@type": "property", "@value": value, "@id": self.getRelatedNode(key)}
        #
        #     # if value is of type dict
        #     elif isinstance(value, dict) and not isinstance(key, int) and not isinstance(key, float):
        #         valueDict = {}
        #
        #         # adding @id to the value dictionary
        #         if key in tempRelatedNodeDict:
        #             finalJson['@id'] = tempRelatedNodeDict[key]
        #             finalContext[key] = tempRelatedNodeDict[key]
        #         elif key not in tempRelatedNodeDict:
        #             finalJson['@id'] = self.getRelatedNode(key)
        #             finalContext[key] = self.getRelatedNode(key)
        #             tempRelatedNodeDict[key] = self.getRelatedNode(key)
        #
        #         # checking whether dict has @type by default or not
        #         for item in value:
        #             if not bool(re.match('.*type?', str(item))) and not bool(re.match('.*value?', str(item))):
        #                 valueDict[item] = value[item]
        #
        #         # checking whether dict has @value by default or not and constructing valueDict
        #         if 'value' in value and len(valueDict) == 0:
        #             valueDict = value['value']
        #         elif 'value' in value and len(valueDict) != 0:
        #             valueDict['value'] = value['value']
        #         else:
        #             value['value'] = valueDict
        #
        #         # tempRelatedNodeDict[key] = self.getRelatedNode(key)
        #
        #         # if json file contains @type
        #         if any(match for match in [re.match(".*type?", i) for i in value]):
        #             tempType = value[[re.findall(".*type?", j) for j in value][0][0]]
        #
        #             # adding @id and @type to dictionary values
        #             if key not in tempRelatedNodeDict:
        #                 finalJson[key] = {"@type": tempType, "@id": self.getRelatedNode(key)}
        #             elif key in tempRelatedNodeDict:
        #                 finalJson[key] = {"@type": tempType, "@id": tempRelatedNodeDict[key]}
        #
        #             # adding @value to dictionary values
        #             finalJson[key]['@value'] = valueDict
        #
        #         # if json file does not contain @type
        #         else:
        #             if self.isClassNode(finalContext[key]):
        #                 finalJson[key] = {"@type": "Relationship", "@value": value['value'],
        #                                   "@id": self.getRelatedNode(key)}
        #             else:
        #                 finalJson[key] = {"@type": "Property", "@value": value['value'],
        #                                   "@id": self.getRelatedNode(key)}
        #
        #         # for adding metadata for keys within a dictionary value
        #         for item in value:
        #             if item not in finalJson["@context"] and item not in tempRelatedNodeDict:
        #                 finalJson["@context"][item] = self.getRelatedNode(item)
        #                 tempRelatedNodeDict[item] = self.getRelatedNode(item)
        #             elif item not in finalJson["@context"] and item in tempRelatedNodeDict:
        #                 finalJson["@context"][item] = tempRelatedNodeDict[item]
        #
        # # this section adds @id to the jsonld file in case initial json doesnt have one
        # if not hasID:
        #     secondLayer = SecondLayer(self.keywords, self.ontologyFilePath, self.fileJsonObject)
        #     secondLayer.generateSecondLayerResultList()
        #     self.featureVector.setPopularityFeatures()
        #     for item in self.featureVector.getQueryURIsTuples():
        #         print(item, self.featureVector.getQueryURIsTuples()[item])
        #     self.featureVector.generateFinalURIs()
        #     print("size of query uris is :", len(queryURIs))
        #     print("most frequent URI is : {} with {} repetitions".format(self.featureVector.most_frequent(queryURIs),
        #                                                                  queryURIs.count(
        #                                                                      self.featureVector.most_frequent(
        #                                                                          queryURIs))))
        #     if len(queryURIs) > 0:
        #         if self.isClassNode(self.most_frequent(queryURIs)):
        #             finalJson['@id'] = self.most_frequent(queryURIs)
        #         else:
        #             finalJson['@id'] = self.getClassNode(self.most_frequent(queryURIs))
        # return finalJson

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
                relatedNode = self.getRelatedNode(key)
                if relatedNode != "" and relatedNode is not None:
                    self.finalContext[key] = relatedNode

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
