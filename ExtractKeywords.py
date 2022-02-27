import re
import json
import xmltodict


class ExtractKeywords:
    keywords = list()
    inputJsonDict = dict

    def __init__(self, fileAddress):
        self.fileAddress = fileAddress

    # returns a list of all key words in the JSON file
    def getAllKeywords(self):
        fh = open(self.fileAddress)

        # JSON format
        if self.isValidJSON() and self.fileAddress.split(' ')[-1].split('.')[-1].lower() == 'json':
            self.inputJsonDict = json.load(fh)
            self.jsonExtractor(self.inputJsonDict)
            return [self.keywords, self.inputJsonDict]

        # XML format
        elif self.fileAddress.split(' ')[-1].split('.')[-1] == 'xml':
            self.inputJsonDict = xmltodict.parse(fh.read())
            self.xmlExtractor(self.inputJsonDict)
            return [self.keywords, self.inputJsonDict]

        # Unstructured data
        else:
            self.inputJsonDict = json.load(fh)
            self.jsonExtractor(self.convertUnstructuredToJson(fh))
            print(self.keywords)
            return [self.keywords, self.inputJsonDict]

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

        arrayObjects = re.findall(r'[^,\{\}]*\[[^\]\{\}]+\]', fileStr)
        arrayObjects = [re.sub('[\"\'\n]', '', arrayObject).strip() for arrayObject in arrayObjects]
        # arrayObjects = [re.sub('([\w]+)', r'"\1"', arrayObject) for arrayObject in arrayObjects]
        arrayObjects = [re.sub(':"\[', r':[', arrayObject) for arrayObject in arrayObjects]

        jsonObjects = re.findall(r'[^,]*\{[^\}]+\}', fileStr)
        jsonObjects = [re.sub('[\"\'\n]', '', jsonObject).strip() for jsonObject in jsonObjects]

        stringObjects = re.findall(r'[^,\{\}\[\]]+[:=][^,\{\}\[\]]+', fileStr)
        stringObjects = [re.sub('[\"\'\n]', '', stringObject).strip() for stringObject in stringObjects]
        stringObjects = [re.sub('[=]', ':', stringObject).strip() for stringObject in stringObjects]

        finalJson = {}
        for item in arrayObjects:
            finalJson[re.sub('"', '' ,re.split(r':\[', item)[0]).strip()] = \
                [item.strip() for item in re.findall('[\w]+:[\w]+',re.split(r':\[', item)[-1])]
            print(finalJson)
        for item in jsonObjects:
            finalJson[re.sub('"', '', re.split(r':\{', item)[0]).strip()] = \
                [item.strip() for item in re.findall('[\w]+:[\w]+',re.split(r':\{', item)[-1])]
        for item in stringObjects:
            finalJson[item.split(':')[0]] = item.split(':')[-1].strip()
        # print(json.dumps(finalJson, indent=4))
        return finalJson

