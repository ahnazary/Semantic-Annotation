import json
import os

from flask import Flask, flash, request, redirect, url_for, session
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
API_UPLOAD_FOLDER = PROJECT_PATH + "/ApiOutputs"
Files_FOLDER = PROJECT_PATH + "/files/*"
API_Files_FOLDER = PROJECT_PATH + "/ApiInputFiles/"
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
        app.secret_key = 'super secret key'
        app.config['SESSION_TYPE'] = 'filesystem'
        app.debug = True
        app.run(port=2000, use_reloader=False)

    @staticmethod
    def allowedFile(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    @app.route("/jsonld", methods=["POST", "GET"])
    def getAnnotatedJsonld():
        # in case a json object is posted to the api
        if request.is_json and request.method == 'POST':
            inputJson = request.get_json()
            tempFile = API_UPLOAD_FOLDER + "/sentFile.json"
            with open(tempFile, 'w') as f:
                json.dump(inputJson, f, indent=4)
            return MyApi.annotateFile(tempFile, outputType='api', outputFormat='jsonld')

        # in case a file is posted to the api
        elif request.method == 'POST':

            # check if the post request has the file part
            if len(request.files) == 0:
                flash('No file part')
                return redirect(request.url)

            # file = request.files['file']
            for key, file in request.files.items():
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)

                if file and MyApi.allowedFile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(API_Files_FOLDER + filename)
                    return MyApi.annotateFile(API_Files_FOLDER + filename, outputType='api', outputFormat='jsonld')

    @staticmethod
    @app.route("/turtle", methods=["POST", "GET"])
    def getAnnotatedTurtle():
        if request.is_json and request.method == 'POST':
            inputJson = request.get_json()
            tempFile = API_UPLOAD_FOLDER + "/sentFile.json"
            with open(tempFile, 'w') as f:
                json.dump(inputJson, f, indent=4)
            return MyApi.annotateFile(tempFile, outputType='api', outputFormat='turtle')

        # in case a file is posted to the api
        elif request.method == 'POST':

            # check if the post request has the file part
            if len(request.files) == 0:
                flash('No file part')
                return redirect(request.url)

            # file = request.files['file']
            for key, file in request.files.items():
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)

                if file and MyApi.allowedFile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(API_Files_FOLDER + filename)
                    return MyApi.annotateFile(API_Files_FOLDER + filename, outputType='api', outputFormat='turtle')

    @staticmethod
    @app.route("/owl", methods=["POST", "GET"])
    def getAnnotatedOwl():
        if request.is_json and request.method == 'POST':
            inputJson = request.get_json()
            tempFile = API_UPLOAD_FOLDER + "/sentFile.json"
            with open(tempFile, 'w') as f:
                json.dump(inputJson, f, indent=4)
            return MyApi.annotateFile(tempFile, outputType='api', outputFormat='owl')

        # in case a file is posted to the api
        elif request.method == 'POST':

            # check if the post request has the file part
            if len(request.files) == 0:
                flash('No file part')
                return redirect(request.url)

            # file = request.files['file']
            for key, file in request.files.items():
                # If the user does not select a file, the browser submits an empty file without a filename.
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)

                if file and MyApi.allowedFile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(API_Files_FOLDER + filename)
                    return MyApi.annotateFile(API_Files_FOLDER + filename, outputType='api', outputFormat='owl')

    # this method either writes output as a file or returns a jsonld, turtle or owl
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
            # if jsonld is requested as the output
            if kwargs['outputFormat'] == 'jsonld':
                result = outputGenerator.getJSONLDFile(finalJsonObjects)
                MyApi.clearVariables()
                return result

            # if turtle is requested as the output
            elif kwargs['outputFormat'] == 'turtle':
                result = outputGenerator.getTurtleFile(finalJsonObjects)
                MyApi.clearVariables()
                return result

            # if owl is requested as the output
            elif kwargs['outputFormat'] == 'owl':
                result = outputGenerator.getOWLFile(finalJsonObjects)
                MyApi.clearVariables()
                return result

    @staticmethod
    def clearVariables():
        SQLDatabase.removeDuplicateRows()
        queryURIs.clear()
        queryURIsTuples.clear()
        finalURIs.clear()
        ExtractKeywords.keywords.clear()

