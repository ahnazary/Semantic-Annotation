import json


class ReadJSON:
    keywords = list()

    def __init__(self, fileAddress):
        self.fileAddress = fileAddress

    # returns a list of all key words in the JSON file
    def getAllKeywords(self):
        fh = open(self.fileAddress)
        jsonData = json.load(fh)
        self.jsonExtractor(jsonData)
        return self.keywords

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