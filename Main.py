import json
import os
import time
import glob

from FirstLayer import FirstLayer
from ExtractKeywords import ExtractKeywords

from FeatureVector import queryURIs, queryURIsTuples, finalURIs, FeatureVector
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec
from OutputGenerator import OutputGenerator

start_time = time.time()

SQLDatabase.readPDFSIntoSQLTable()
myThing = MyWord2Vec()
MyWord2Vec.startTokenizingInputText(SQLDatabase.readPDFContentsIntoASingleString())

projectPath = os.path.abspath(os.path.dirname(__file__))
path = projectPath + "/files/*"

for file in glob.glob(path):
    SQLDatabase.removeDuplicateRows()
    print('\n', file)
    filePath = file
    filePathOntology = projectPath + "/AllFiles/sargon.ttl"

    extractKeywords = ExtractKeywords(filePath)
    allKeywords = extractKeywords.getAllKeywords()[0]
    fileJsonObject = extractKeywords.getAllKeywords()[1]

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()
    SQLDatabase.createOuterNodeTable()

    firstLayer = FirstLayer(allKeywords, filePathOntology, fileJsonObject, jsonldValuesFormat='array')

    outputGenerator = OutputGenerator(file, finalURIs)

    finalJsonObjects = firstLayer.buildFinalJson()
    outputGenerator.writeJSONLDFileFromDict(finalJsonObjects)
    outputGenerator.writeTurtleFile(finalJsonObjects)
    outputGenerator.writeOWLFile(finalJsonObjects)

    # outputGenerator.writeTurtleFile(
    #     {
    #         "@context": {
    #             "device": "https://w3id.org/saref#Device",
    #             "ts": "http://webprotege.stanford.edu/Timestamp",
    #             "UL1m": "http://webprotege.stanford.edu/Maqnititute",
    #             "hasChannel": "http://webprotege.stanford.edu/hasChannel",
    #             "UL1a": "http://webprotege.stanford.edu/Angle",
    #             "UL1f": "http://webprotege.stanford.edu/Frequency",
    #             "IL1m": "http://webprotege.stanford.edu/Maqnititute",
    #             "IL1a": "http://webprotege.stanford.edu/Angle",
    #             "IL1f": "http://webprotege.stanford.edu/Frequency",
    #             "UL2m": "http://webprotege.stanford.edu/Maqnititute",
    #             "UL2a": "http://webprotege.stanford.edu/Angle",
    #             "UL2f": "http://webprotege.stanford.edu/Frequency",
    #             "IL2m": "http://webprotege.stanford.edu/Maqnititute",
    #             "IL2a": "http://webprotege.stanford.edu/Angle",
    #             "IL2f": "http://webprotege.stanford.edu/Frequency",
    #             "UL3m": "http://webprotege.stanford.edu/Maqnititute",
    #             "UL3a": "http://webprotege.stanford.edu/Angle",
    #             "UL3f": "http://webprotege.stanford.edu/Frequency",
    #             "IL3m": "http://webprotege.stanford.edu/Maqnititute",
    #             "IL3a": "http://webprotege.stanford.edu/Angle",
    #             "IL3f": "http://webprotege.stanford.edu/Frequency"
    #         },
    #         "@id": "pmu_avacon1",
    #         "@type": "http://webprotege.stanford.edu/PMU",
    #         "device": [
    #             {"@id": "device"},
    #             {"@value": "pmu_avacon1",
    #              "@type": "https://w3id.org/saref#Device"}
    #         ],
    #         "ts": {
    #             "@id": "ts",
    #             "@value": "2021-11-17T14:23:19.999921+00:00",
    #             "@type": "http://webprotege.stanford.edu/Timestamp"
    #         },
    #         "hasChannel": [
    #             {"@type": "http://webprotege.stanford.edu/hasChannel"},
    #             {"UL1m": [
    #                 {"@id": "UL1m"},
    #                 {"@value": 225.656173706055,
    #                 "@type": "http://webprotege.stanford.edu/Maqnititute"}
    #             ]},
    #             {"IL1m": [
    #                 {"@id": "IL1m"},
    #                 {"@value": 0.909491896629334,
    #                 "@type": "http://webprotege.stanford.edu/Maqnititute"}
    #             ]},
    #         ]
    #     })

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    finalURIs.clear()
    extractKeywords.keywords.clear()

print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
