import json
import os

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from FirstLayer import FirstLayer
from MyWord2Vec import MyWord2Vec
from OutputGenerator import OutputGenerator
from SQLDatabase import SQLDatabase
from FeatureVector import queryURIs, queryURIsTuples, finalURIs
from ExtractKeywords import ExtractKeywords


# folder paths which contain inputs and outputs
ALLOWED_EXTENSIONS = {'csv', 'json', 'xml'}
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
API_UPLOAD_FOLDER = PROJECT_PATH+ "/ApiOutputs"
Files_FOLDER = PROJECT_PATH + "/files/*"
API_Files_FOLDER = PROJECT_PATH + "/files/*"
ONTOLOGY_File_PATH = PROJECT_PATH + "/AllFiles/sargon.ttl"


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = API_UPLOAD_FOLDER


class MyApi:
    def __init__(self):
        self.jsonld = None
        self.turtle = None
        self.owl = None

    @staticmethod
    def initAPI():
        app.run(debug=True, port=2000, use_reloader=False)


    def allowedFile(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    @app.route("/json-ld", methods=["POST", "GET"])
    def getAnnotatedJsonld():
        if request.is_json and request.method == 'POST':
            inputJson = request.get_json()
            tempFile = API_UPLOAD_FOLDER + "/sentFile.json"
            with open(tempFile, 'w') as f:
                json.dump(inputJson, f, indent=4)
            return MyApi.annotateFile(tempFile, outputType='api', outputFormat='jsonld')

    @staticmethod
    def annotateFile(inputFile, **kwargs):
        SQLDatabase.removeDuplicateRows()
        print('\n', inputFile)
        filePath = inputFile

        extractKeywords = ExtractKeywords(filePath)
        allKeywords = extractKeywords.getAllKeywords()[0]
        fileJsonObject = extractKeywords.getAllKeywords()[1]

        SQLDatabase.createKeywordsTable()
        SQLDatabase.createURIsParentsTable()
        SQLDatabase.createOuterNodeTable()

        firstLayer = FirstLayer(allKeywords, ONTOLOGY_File_PATH, fileJsonObject, jsonldValuesFormat='dict')

        outputGenerator = OutputGenerator(inputFile, finalURIs)

        finalJsonObjects = firstLayer.buildFinalJson()
        if kwargs['outputType'].lower() == 'file':
            outputGenerator.writeJSONLDFile(finalJsonObjects)
            outputGenerator.writeTurtleFile(finalJsonObjects)
            outputGenerator.writeOWLFile(finalJsonObjects)

        elif kwargs['outputType'].lower() == 'api':
            if kwargs['outputFormat'] == 'jsonld':
                result = outputGenerator.getJSONLDFile(finalJsonObjects)
                MyApi.clearVariables()
                return result


    @staticmethod
    def clearVariables():
        SQLDatabase.removeDuplicateRows()
        queryURIs.clear()
        queryURIsTuples.clear()
        finalURIs.clear()
        ExtractKeywords.keywords.clear()