from termcolor import colored

from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs, queryURIsTuples
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/Sargon.ttl":
            self.ontologyStr = "SARGON"
        if ontology == "/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/saref.ttl":
            self.ontologyStr = "SAREF"

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateFirstLayerResultList(self):
        global flag
        layer = "firstLayer"
        for word in self.keywords:
            flag = True
            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            # print(word, "1st")
            if SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                SQLDatabase.queryKeywordFromSQL(word, self.ontologyStr, layer)
            elif not SQLDatabase.keywordExists(word, self.ontologyStr, layer):
                queryStrExact = prefixes + """SELECT ?subject
                    WHERE{
                    {?subject rdfs:label ?object}
                    FILTER (regex(?subject, \"""" + word + "\", \"i\" ) || contains(str(?subject), \'" + word + "\'))}"
                queryResult = self.ontology.query(queryStrExact)
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
                        flag = False

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
                        flag = False

                # if no URI found for the keyword
                if flag:
                    SQLDatabase.addToKeywords(word, self.ontologyStr, layer, None, None, None)
                    str = 'No URI found for: ' + word + " in the Ontology"
                    # print(colored(str, 'magenta'))
        # SQLDatabase.removeDuplicateRows()