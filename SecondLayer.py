from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs


class SecondLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateSecondLayerResultList(self):
        for word in self.keywords:

            # for fullWord in self.keywords:
            #     for sub in fullWord.split(":"):
            #         if FeatureVector.isBoolean(self, sub) or FeatureVector.isNumber(self, sub):
            #             word = fullWord.replace(sub, "")
            #             print(word)
            #     print(word)

            word = ''.join([i for i in word if not i.isdigit() and not i == ":"])
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            print(word)

            queryStrExact = prefixes + """SELECT ?subject
               WHERE{
               {?subject rdfs:comment ?object} UNION{
               ?subject rdfs:label ?object}
               FILTER regex(?object, \"""" + word + "\", \"i\" )}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                temp = FeatureVector.isClassNode(self, f"{row.subject}")
                if temp and f"{row.subject}" not in bannedURIs:
                    print(f"{row.subject}", temp)
                    queryURIs.append(f"{row.subject}")
                if not temp and f"{row.subject}" not in bannedURIs:
                    print(f"{row.subject}", temp)
                    print("   ", FeatureVector.getClassNode(self, f"{row.subject}"))

        for word in self.keywords:
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            for i in range(0, len(word) + 1, 1):
                for j in range(i + 3, len(word) + 1, 1):
                    subString = word[i:j]
                    subString = ''.join([i for i in subString if not i.isdigit() and not i == ":"])
                    if subString in bannedStrings or len(subString) <= 2:
                        continue
                    print(subString)
                    queryStr = prefixes + """SELECT ?subject
                        WHERE{
                        {?subject rdfs:comment ?object} UNION{
                        ?subject rdfs:label ?object}
                         FILTER (regex(?object, \" """ + subString + " \", \"i\" ))}"

                    queryResult = self.ontology.query(queryStr)
                    for row in queryResult:
                        temp = FeatureVector.isClassNode(self, f"{row.subject}")
                        if temp and f"{row.subject}" not in bannedURIs:
                            print(f"{row.subject}", temp)
                            queryURIs.append(f"{row.subject}")
                        if not temp and f"{row.subject}" not in bannedURIs:
                            print(f"{row.subject} ", temp)
                            print("   ", FeatureVector.getClassNode(self, f"{row.subject}"))

