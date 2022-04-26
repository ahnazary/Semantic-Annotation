import os
import time
import glob

from FirstLayer import FirstLayer
from ExtractKeywords import ExtractKeywords
from FeatureVector import queryURIs, queryURIsTuples, finalURIs
from MyApi import MyApi
from SQLDatabase import SQLDatabase
from MyWord2Vec import MyWord2Vec
from OutputGenerator import OutputGenerator

# folder paths which contain inputs, outputs and ontology files
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
API_UPLOAD_FOLDER = PROJECT_PATH+ "/ApiOutputs"
Files_FOLDER = PROJECT_PATH + "/files/*"
API_Files_FOLDER = PROJECT_PATH + "/files/*"
ONTOLOGY_File_PATH = PROJECT_PATH + "/AllFiles/sargon.ttl"


# function that annotates an input file using a given ontology
def annotateFile(inputFileAddress, *arg, **kwargs):
    SQLDatabase.removeDuplicateRows()
    print('\n', inputFileAddress)
    filePath = inputFileAddress

    extractKeywords = ExtractKeywords(filePath)
    allKeywords = extractKeywords.getAllKeywords()[0]
    fileJsonObject = extractKeywords.getAllKeywords()[1]

    SQLDatabase.createKeywordsTable()
    SQLDatabase.createURIsParentsTable()
    SQLDatabase.createOuterNodeTable()

    # jsonldValuesFormat can be either 'array' or 'dict'
    firstLayer = FirstLayer(allKeywords, ONTOLOGY_File_PATH, fileJsonObject, jsonldValuesFormat='array')

    outputGenerator = OutputGenerator(inputFileAddress, finalURIs)

    finalJsonObjects = firstLayer.buildFinalJson()
    if kwargs['outputType'].lower() == 'file':
        outputGenerator.writeJSONLDFile(finalJsonObjects)
        outputGenerator.writeTurtleFile(finalJsonObjects)
        outputGenerator.writeOWLFile(finalJsonObjects)

    elif kwargs['outputType'].lower() == 'api':
        arg.jsonld = outputGenerator.getJSONLDFile(finalJsonObjects)
        print(arg.jsonld)

    SQLDatabase.removeDuplicateRows()
    queryURIs.clear()
    queryURIsTuples.clear()
    finalURIs.clear()
    extractKeywords.keywords.clear()


if __name__ == '__main__':
    start_time = time.time()

    SQLDatabase.readPDFSIntoSQLTable()
    myThing = MyWord2Vec()
    MyWord2Vec.startTokenizingInputText(SQLDatabase.readPDFContentsIntoASingleString())

    # # annotating files in the file
    # for inputFile in glob.glob(Files_FOLDER):
    #     annotateFile(inputFile, outputType='file')

    myAPi = MyApi()
    myAPi.initAPI()

    # # annotating files in the Files_FOLDER
    # for inputFile in glob.glob(API_Files_FOLDER):
    #     annotateFile(outputType='api')

    print("Total runtime is : " + " %s seconds " % (time.time() - start_time))
