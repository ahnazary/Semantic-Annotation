from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
import nltk
# nltk.download('punkt')

warnings.filterwarnings(action='ignore')

import gensim
from gensim.models import Word2Vec


j = "description ontology is rstly dened"
print(j)
j = ''.join(char for char in j if char.isalnum())
print(j)

#  Reads ‘alice.txt’ file
sample = open("/home/amirhossein/Documents/GitHub/Semantic-Annotation/text.txt", "r")
s = sample.read()

# Replaces escape character with space
f = s.replace("\n", " ")

data = []

# iterate through each sentence in the file
for i in sent_tokenize(f):
    temp = []

    # tokenize the sentence into words
    for j in word_tokenize(i):
        j = ''.join(char for char in j if char.isalnum())
        temp.append(j.lower())

    data.append(temp)

# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count=1,
                                window=5)

# Print results
keyword = "actuator"
word = "sensor"
try:
    print("Cosine similarity between '" + keyword + "' " +
          "and '" + word + "' - CBOW : ",
          model1.wv.similarity(keyword, word))

except:
    print("keyword not found")

# Create Skip Gram model
model2 = gensim.models.Word2Vec(data, min_count=1, window=5, sg=1)

# Print results
try:
    print("Cosine similarity between '" + keyword + "' " +
          "and '" + word + "' - Skip Gram : ",
          model2.wv.similarity(keyword, word))

except:
    print("keyword not found")