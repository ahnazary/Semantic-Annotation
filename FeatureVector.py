import rdflib

prefixes = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX om: <http://www.wurvoc.org/vocabularies/om-1.8/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX time: <http://www.w3.org/2006/time#> 
PREFIX saref: <https://w3id.org/saref#>  
PREFIX saref: <https://saref.etsi.org/core/>  
PREFIX schema: <http://schema.org/>  
PREFIX dcterms: <http://purl.org/dc/terms/>  
PREFIX base: <http://def.isotc211.org/iso19150-2/2012/base#> 
PREFIX oboe-core: <http://ecoinformatics.org/oboe/oboe.1.0/oboe-core.owl#> 
PREFIX sosa: <http://www.w3.org/ns/sosa/> 
PREFIX sosa-om: <http://www.w3.org/ns/sosa/om#> 
PREFIX dc: <http://purl.org/dc/elements/1.1/> 
PREFIX dct: <http://purl.org/dc/terms/> 
PREFIX iso19156-gfi: <http://def.isotc211.org/iso19156/2011/GeneralFeatureInstance#> 
PREFIX iso19156-om: <http://def.isotc211.org/iso19156/2011/Observation#> 
PREFIX iso19156-sf: <http://def.isotc211.org/iso19156/2011/SamplingFeature#> 
PREFIX iso19156-sfs: <http://def.isotc211.org/iso19156/2011/SpatialSamplingFeature#> 
PREFIX iso19156-sp: <http://def.isotc211.org/iso19156/2011/Specimen#> 
PREFIX iso19156_gfi: <http://def.isotc211.org/iso19156/2011/GeneralFeatureInstance#> 
PREFIX iso19156_sf: <http://def.isotc211.org/iso19156/2011/SamplingFeature#> 
PREFIX xml: <http://www.w3.org/XML/1998/namespace> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX terms: <http://purl.org/dc/terms/> 
PREFIX vann: <http://purl.org/vocab/vann/> 
PREFIX webprotege: <http://webprotege.stanford.edu/> 
PREFIX : <https://w3id.org/saref#> \n"""
bannedStrings = ["type",
                 "unit",
                 "measure",
                 "relation",
                 "value",
                 "relationship",
                 "property",
                 "the",
                 "has",
                 "and",
                 "add"]
bannedURIs = ["https://w3id.org/saref",
              "http://www.w3.org/ns/sosa/om"]
queryURIs = [""]


class FeatureVector:

    def __init__(self, keywords, ontology):
        self.keywords = keywords
        self.ontology = ontology
        self.ontology = rdflib.Graph()
        self.ontology.parse(ontology)

    def getPrefName(self, nodeName):

        queryString = prefixes + """select ?subject (group_concat(?prefixedName ; separator = \"\") as ?prefName) where{
             values (?prefix ?ns) { 
             ( \":\" <https://w3id.org/saref#> )
             ( \"saref:\" <https://w3id.org/saref#> )
             ( \"saref:\" <https://saref.etsi.org/core/> )
             ( \"xsd:\" <http://www.w3.org/2001/XMLSchema#> )
             ( \"rdfs:\" <http://www.w3.org/2000/01/rdf-schema#> )
             ( \"owl:\" <http://www.w3.org/2002/07/owl#> )
             ( \"foaf:\" <http://xmlns.com/foaf/0.1/> )
             ( \"time:\" <http://www.w3.org/2006/time#> )
             ( \"schema:\" <http://schema.org/> )
             ( \"dcterms:\" <http://purl.org/dc/terms/> )
             ( \"om:\" <http://www.wurvoc.org/vocabularies/om-1.8/> )
             ( \"rdf:\" <http://www.w3.org/1999/02/22-rdf-syntax-ns#> )
             ( \"dc:\" <http://purl.org/dc/elements/1.1/> )
             ( \"dct:\" <http://purl.org/dc/terms/> )
             ( \"iso19156-gfi:\" <http://def.isotc211.org/iso19156/2011/GeneralFeatureInstance#> )
             ( \"iso19156-om:\" <http://def.isotc211.org/iso19156/2011/Observation#> )
             ( \"iso19156-sf:\" <http://def.isotc211.org/iso19156/2011/SamplingFeature#> )
             ( \"iso19156-sfs:\" <http://def.isotc211.org/iso19156/2011/SpatialSamplingFeature#> )
             ( \"iso19156-sp:\" <http://def.isotc211.org/iso19156/2011/Specimen#> )
             ( \"iso19156_gfi:\" <http://def.isotc211.org/iso19156/2011/GeneralFeatureInstance#> )
             ( \"iso19156_sf:\" <http://def.isotc211.org/iso19156/2011/SamplingFeature#> )
             ( \"sosa-om:\" <http://www.w3.org/ns/sosa/om#> )
             ( \"oboe-core:\" <http://ecoinformatics.org/oboe/oboe.1.0/oboe-core.owl#> )
             ( \"webprotege:\" <http://webprotege.stanford.edu/> )
             ( \"terms:\" <http://purl.org/dc/terms/> )
             ( \"skos:\" <http://www.w3.org/2004/02/skos/core#> )
             ( \"vann:\" <http://purl.org/vocab/vann/> )
             ( \"xml:\" <http://www.w3.org/XML/1998/namespace> )}
             ?subject rdfs:label ?object.
             FILTER (?subject = <""" + nodeName + """>) 
             bind( if( strStarts( str(?subject), str(?ns) ),
             concat( ?prefix, strafter( str(?subject), str(?ns) )),
             \"\" ) 
             as ?prefixedName )}
             group by ?subject
             order by ?subject"""

        queryResult = self.ontology.query(queryString)
        for row in queryResult:
            return f"{row.prefName}".split(" ")[0]

    def getClassNode(self, nodeName):
        result = list()
        nodePrefName = self.getPrefName(nodeName)
        queryString = prefixes + """SELECT ?subject
           WHERE{
           {?subject ?predicate ?object}
           FILTER (?object =""" + nodePrefName + ")}"

        queryStringBlankNode = prefixes + """SELECT ?subject
           WHERE{
           {?subject ?a [?b ?object]}
           FILTER (?object =""" + nodePrefName + ")}"

        queryResult = self.ontology.query(queryString)
        queryResultBlankNode = self.ontology.query(queryStringBlankNode)

        for row in queryResult:
            if "\\" not in f"{row.subject}" or "http" not in f"{row.subject}" or "www" not in f"{row.subject}":
                for row in queryResultBlankNode:
                    print(f"{row.subject}")
                    result.append(f"{row.subject}")
                return result
            else:
                print(f"{row.subject}")
                result.append(f"{row.subject}")
        return result

        # if len(queryResult) > len(queryResultBlankNode):
        #     for row in queryResult:
        #         print(f"{row.subject}")
        #         result.append(f"{row.subject}")
        #     return result
        #
        # if len(queryResult) < len(queryResultBlankNode):
        #     for row in queryResultBlankNode:
        #         print(f"{row.subject}")
        #         result.append(f"{row.subject}")
        #     return result
        #
        # if len(queryResult) == len(queryResultBlankNode) == 1:
        #     for row in queryResult:
        #         if '\\' in f"{row.subject}" or "http" in f"{row.subject}" or "www" in f"{row.subject}":
        #             print(f"{row.subject}")
        #             result.append(f"{row.subject}")
        #
        #     for row in queryResultBlankNode:
        #         if '\\' in f"{row.subject}" or "http" in f"{row.subject}" or "www" in f"{row.subject}":
        #             print(f"{row.subject}")
        #             result.append(f"{row.subject}")
        #     return result
        #
        # else:
        #     for row in queryResult:
        #         print(f"{row.subject}")
        #     for row in queryResultBlankNode:
        #         print(f"{row.subject}")
        #     print("Something unknown happened!")

    def isClassNode(self, nodeName):
        queryString = prefixes + """SELECT ?object
           WHERE{
           {?subject rdf:type ?object}
           FILTER (?subject =  """ + nodeName + ")}"

        queryResult = self.ontology.query(queryString)
        for row in queryResult:
            print(f"{row.object} ")
            if f"{row.object}" == "http://www.w3.org/2002/07/owl#Class" or f"{row.object}" == "owl:class":
                return True
            else:
                return False

    @staticmethod
    def getQueryURIs():
        return queryURIs

    @staticmethod
    def getPrefixes(self):
        return prefixes

    @staticmethod
    def getBannedStrings(self):
        return bannedStrings
