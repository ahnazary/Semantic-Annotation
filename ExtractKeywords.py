import re
import json
import xmltodict


class ExtractKeywords:
    keywords = list()

    def __init__(self, fileAddress):
        self.fileAddress = fileAddress

    # returns a list of all key words in the JSON file
    def getAllKeywords(self):
        fh = open(self.fileAddress)
        if self.isValidJSON() and self.fileAddress.split(' ')[-1].split('.')[-1].lower() == 'json':
            jsonData = json.load(fh)
            self.jsonExtractor(jsonData)
            return self.keywords
        elif self.fileAddress.split(' ')[-1].split('.')[-1] == 'xml':
            xmlData = xmltodict.parse(fh.read())
            self.xmlExtractor(xmlData)
            return self.keywords
        # Unstructured data
        else:
            self.convertUnstructuredToJson(fh)


    def jsonExtractor(self, inputJSON):
        for entry in inputJSON:
            self.keywords.append(str(entry))
            if isinstance(inputJSON[entry], str):
                self.keywords.append(str(inputJSON[entry]))
            if isinstance(inputJSON[entry], list):
                for i in inputJSON[entry]:
                    self.keywords.append(str(i))
            if isinstance(inputJSON[entry], dict):
                self.jsonExtractor(inputJSON[entry])

    def xmlExtractor(self, inputXML):
        for entry in inputXML:
            if isinstance(entry, str):
                self.keywords.append(entry)
            if isinstance(inputXML[entry], str):
                self.keywords.append(inputXML[entry])
            elif isinstance(inputXML[entry], dict):
                self.xmlExtractor(inputXML[entry])

    def isValidJSON(self):
        try:
            with open(self.fileAddress) as f:
                return True
        except ValueError as e:
            return False

    @staticmethod
    def convertUnstructuredToJson(fileHandle):
        fileStr = fileHandle.read().strip()
        re1 = r'\[\" ]*[\w]*[\ ]*:\[\" ][\w]*[\" ]*'
        re1 = r'[^\[\]]*[\w"]+:[\w" ]+'
        # generic_re = re.compile("(%s)" % (re1)).findall(fileStr)
        arrayObjects = re.findall(r'[^, ]*\[[^\]]*\]', fileStr)
        arrayObjects = [re.sub('\"\'', '', arrayObject) for arrayObject in arrayObjects]
        print(arrayObjects, len(arrayObjects))
        jsonObjects = re.findall(r'[^, ]*\{[^\}]*\}', fileStr)
        jsonObjects = [re.sub('\"\'','',jsonObject) for jsonObject in jsonObjects]
        print(jsonObjects, len(jsonObjects))