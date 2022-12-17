FROM python:latest

WORKDIR /SiSEG

RUN pip install -r requirements.txt

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
