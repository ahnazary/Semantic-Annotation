from FeatureVector import FeatureVector, prefixes, queryURIs, bannedStrings,bannedURIs


class FirstLayer(FeatureVector):
    def __init__(self, keywords, ontology):
        super().__init__(keywords, ontology)

    # this method creates a list of all queried URIs which will be use to calculate popularity
    def generateFirstLayerResultList(self):
        for word in self.keywords:
            print(word)
            if word.lower()  in bannedStrings or len(word) <= 2:
                continue
            queryStrExact = prefixes + """SELECT ?subject
                WHERE{
                {?subject rdfs:label ?object}
                FILTER (regex(?object, \"""" + word + "\" ) || contains(str(?subject), \'" + word + "\'))}"
            queryResult = self.ontology.query(queryStrExact)
            for row in queryResult:
                print(f"{row.subject} ")
                if f"{row.subject} " not in bannedURIs:
                    queryURIs.append(f"{row.subject}")
