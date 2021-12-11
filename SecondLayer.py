from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings, bannedURIs


class SecondLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateSecondLayerResultList(self):
        for word in self.keywords:
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            print(word)
            queryStrExact = prefixes + """SELECT ?subject
               WHERE{
               {?subject rdfs:comment ?object}
               FILTER (regex(?object, \"""" + word + "\", \"i\" ))}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                print(f"{row.subject} ")
                if f"{row.subject} " not in bannedURIs:
                    queryURIs.append(f"{row.subject}")

        for word in self.keywords:
            if word.lower() in bannedStrings or len(word) <= 2:
                continue
            for i in range(0, len(word) + 1, 1):
                for j in range(i + 3, len(word) + 1, 1):
                    subString = word[i:j]
                    if subString in bannedStrings or len(word) <= 2:
                        continue
                    print(subString)
                    queryStr = prefixes + """SELECT ?subject
                                WHERE{
                                {?subject rdfs:comment ?object}
                                 FILTER (regex(?object, \" """ + subString + " \", \"i\" ))}"

                    queryResult = self.ontology.query(queryStr)
                    for row in queryResult:
                        print(f"{row.subject} ")
                        if f"{row.subject} " not in bannedURIs:
                            queryURIs.append(f"{row.subject}")
