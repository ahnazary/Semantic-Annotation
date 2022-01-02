from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import gensim
from gensim.models import Word2Vec

warnings.filterwarnings(action='ignore')
data = []


class MyWord2Vec:

    @staticmethod
    def startTokenizingInputText(text):
        # Replaces escape character with space
        f = text.replace("\n", " ")
        # iterate through each sentence in the file
        for i in sent_tokenize(f):
            temp = []
            # tokenize the sentence into words
            for j in word_tokenize(i):
                j = ''.join(char for char in j if char.isalnum())
                temp.append(j.lower())
            data.append(temp)

    @staticmethod
    # Create CBOW model
    def getCBOW(keyword, word):
        f = open("/home/amirhossein/Documents/GitHub/Semantic-Annotation/files/text.txt", 'r')
        model1 = gensim.models.Word2Vec(data, min_count=1, window=20)
        # print results
        try:
            print("Cosine similarity between '" + keyword + "' " +
                  "and '" + word + "' - CBOW : ",
                  model1.wv.similarity(keyword.lower(), word.lower()))
            return model1.wv.similarity(keyword.lower(), word.lower())
        except:
            print("keyword not found")
            return 0.2

    @staticmethod
    # Create Skip Gram model
    def getSkipGram(keyword, word):
        model2 = gensim.models.Word2Vec(data, min_count=1, window=5, sg=1)
        # Print results
        try:
            print("Cosine similarity between '" + keyword + "' " +
                  "and '" + word + "' - Skip Gram : ",
                  model2.wv.similarity(keyword.lower(), word.lower()))
        except:
            print("keyword not found")
