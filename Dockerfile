FROM python:latest

WORKDIR /SiSEG

RUN apt-get update
RUN pip install rdflib
RUN pip install termcolor
RUN pip install pdfplumber
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install nltk
RUN pip install gensim
RUN pip install pandas
RUN pip install xmltodict
RUN pip install flask
RUN pip install waitress

ADD Main.py ./
ADD ExtractKeywords.py ./
ADD FeatureVector.py ./
ADD FirstLayer.py ./
ADD MyApi.py ./
ADD MyWord2Vec.py ./
ADD OutputGenerator.py ./
ADD SecondLayer.py ./
ADD SQLDatabase.py ./
ADD SVM.py ./

COPY ./AllFiles ./AllFiles
COPY ./URIs.sqlite ./URIs.sqlite
COPY ./nltk_data /root/nltk_data
COPY ./files ./files
COPY ./Outputs ./Outputs
COPY ./ApiOutputs ./ApiOutputs
COPY ./ApiInputFiles ./ApiInputFiles


CMD [ "python", "Main.py" ]
