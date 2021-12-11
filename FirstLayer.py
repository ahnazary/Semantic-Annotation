from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)

    def generateFirstLayerResultList(self):
        for word in self.keywords:
            print(word)
            if word in bannedStrings or len(word) <= 2:
                continue
            queryStrExact = prefixes + """SELECT ?subject
                        WHERE{
                        {?subject rdfs:label ?object}
                        FILTER (regex(?object, \"""" + word + "\" ) || contains(str(?subject), \'" + word + "\'))}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                print(f"{row.subject} ")
                queryURIs.append(f"{row.subject}")

        for word in self.keywords:
            if word in bannedStrings or len(word) <= 2:
                continue
            for i in range(0, len(word) + 1, 1):
                for j in range(i + 3, len(word) + 1, 1):
                    subString = word[i:j]
                    if subString in bannedStrings or len(word) <= 2:
                        continue
                    print(subString)
                    queryStr = prefixes + """SELECT ?subject
                                WHERE{
                                {?subject rdfs:label ?object}
                                filter (regex(str(?object), \' """ + subString + "\') || contains(str(?subject), \'" + subString + "\')) }"

                    queryResult = self.ontology.query(queryStr)
                    for row in queryResult:
                        print(f"{row.subject} ")
