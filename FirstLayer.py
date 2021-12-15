from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings,bannedURIs


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateFirstLayerResultList(self):
        for word in self.keywords:
            word = ''.join([i for i in word if not i.isdigit() or not i == ":"])
            print(word)
            if word.lower()  in bannedStrings or len(word) <= 2:
                continue
            queryStrExact = prefixes + """SELECT ?subject
                WHERE{
                {?subject rdfs:label ?object}
                FILTER (regex(?object, \"""" + word + "\" ) || contains(str(?subject), \'" + word + "\'))}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                temp = FeatureVector.isClassNode(self, f"{row.subject}")
                if temp and f"{row.subject}" not in bannedURIs:
                    print(f"{row.subject}", temp)
                    queryURIs.append(f"{row.subject}")
                if not temp and f"{row.subject}" not in bannedURIs:
                    print(f"{row.subject} ", temp)
                    print("   ", FeatureVector.getClassNode(self, f"{row.subject}"))
