from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import gensim
import re
from gensim.models import Word2Vec
from FeatureVector import bannedStrings

warnings.filterwarnings(action='ignore')
data = []


class MyWord2Vec:

    @staticmethod
    def startTokenizingInputText(text):
        print("Started tokenizing corpus text ...")
        # Replaces escape character with space
        f = text.replace("\n", " ")
        # iterate through each sentence in the file
        for i in sent_tokenize(f):
            temp = []
            # tokenize the sentence into words
            for j in word_tokenize(i):
                if len(j) == 1 or len(j) == 0 or j == '':
                    continue
                j = ''.join(char for char in j if char.isalnum())
                temp.append(j.lower())
            data.append(temp)

    @staticmethod
    # Create CBOW model
    def GetCBOW(keyword, word):
        result = []
        if '/' in word:
            word = word.split("/")[-1]
            word = word.split("#")[-1]
            print("word is " + word)
        elif ':' in word:
            word = word.split(":")[-1]
            print("word is " + word)
            print(re.findall('[A-Z][^A-Z]*', word))

        model1 = gensim.models.Word2Vec(data, min_count=1, window=5)
        for subWord in re.findall('[A-Z][^A-Z]*', word):
            if subWord in bannedStrings:
                continue
            try:
                print("Cosine similarity between '" + keyword + "' " +
                      "and '" + subWord + "' - CBOW : ",
                      model1.wv.similarity(keyword.lower(), subWord.lower()))
                result.append(model1.wv.similarity(keyword.lower(), subWord.lower()))
            except KeyError:
                print("keyword not found")
                result.append(0.4)

        # returning the final cosine similarity
        if len(result) == 1:
            return float(result[0])
        if len(result) == 0:
            return float(0.4)
        if len(result) >= 2:
            res = 0.0
            for i in result:
                res += float(i)
            return res / len(result)

    @staticmethod
    # Create Skip Gram model
    def GetSkipGram(keyword, word):
        result = []
        if '/' in word:
            word = word.split("/")[-1]
            word = word.split("#")[-1]
        elif ':' in word:
            word = word.split(":")[-1]
            print("word is " + word)
            print(re.findall('[A-Z][^A-Z]*', word))
        model2 = gensim.models.Word2Vec(data, min_count=1, window=5, sg=1)
        # Print results
        for subWord in re.findall('[A-Z][^A-Z]*', word):
            if subWord in bannedStrings:
                continue
            try:
                print("Cosine similarity between '" + keyword + "' " +
                      "and '" + subWord + "' - Skip Gram : ",
                      model2.wv.similarity(keyword.lower(), subWord.lower()))
                result.append(model2.wv.similarity(keyword.lower(), subWord.lower()))
            except KeyError:
                print("keyword not found")
                result.append(0.4)

        # returning the final cosine similarity
        if len(result) == 1:
            return float(result[0])
        if len(result) == 0:
            return float(0.4)
        if len(result) >= 2:
            res = 0.0
            for i in result:
                res += float(i)
            return res / len(result)
