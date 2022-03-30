import glob
import os
import sqlite3
import pdfplumber

from FeatureVector import queryURIs, queryURIsTuples, prefixes

conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()


class SQLDatabase:
    def __init__(self):
        # constructing outerNodeTable in SQL database
        self.addToOuterNodesTable('https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute', 'SARGON',
                                         'https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/has_channel')
        self.addToOuterNodesTable('https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle', 'SARGON',
                                         'https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/has_channel')
        self.addToOuterNodesTable('https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency', 'SARGON',
                                         'https://sargon-n5geh.netlify.app/ontology/1.0/object_properties/has_channel')

        # adding data for PMUs
        self.addToKeywords('ulm', 'SARGON', 'secondLayer',
                           'https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute', 0.4, 0.4)
        self.addToKeywords('ula', 'SARGON', 'secondLayer',
                           'https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle', 0.4, 0.4)
        self.addToKeywords('ulf', 'SARGON', 'secondLayer',
                           'https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency', 0.4, 0.4)
        self.addToKeywords('ilm', 'SARGON', 'secondLayer',
                           'https://sargon-n5geh.netlify.app/ontology/1.0/classes/Maqnitute', 0.4, 0.4)
        self.addToKeywords('ila', 'SARGON', 'secondLayer',
                           'https://sargon-n5geh.netlify.app/ontology/1.0/classes/Angle', 0.4, 0.4)
        self.addToKeywords('ilf', 'SARGON', 'secondLayer',
                           'https://sargon-n5geh.netlify.app/ontology/1.0/classes/Frequency', 0.4, 0.4)


    @staticmethod
    def createKeywordsTable():
        cur.executescript('''      
           create table if not exists Keywords (
                    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT unique,
                keyword TEXT,
                ontology TEXT,
                layer TEXT,
                URI TEXT,
                CBOW REAL,
                SkipGram REAL,
                UNIQUE (keyword, ontology, layer, URI)
            );
            ''')
        conn.commit()

    @staticmethod
    def createURIsParentsTable():
        cur.executescript('''
           create table if not exists URIsParents (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT unique,
                URI   TEXT unique,
                isClass TEXT,
                parents TEXT,
                UNIQUE (URI, isClass, parents)
            );
            ''')
        conn.commit()

    @staticmethod
    def createOuterNodeTable():
        cur.executescript('''      
           create table if not exists OuterNodesTable (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT unique,
                InnerNode TEXT,
                ontology TEXT,
                outerNode TEXT,
                UNIQUE (InnerNode, ontology, OuterNode)
            );
            ''')
        conn.commit()

    @staticmethod
    def addToOuterNodesTable(innerNode, ontology, outerNode):
        cur.execute('''INSERT OR IGNORE INTO OuterNodesTable (InnerNode, ontology, outerNode)
                    VALUES ( ?, ?, ?)''', (innerNode, ontology, outerNode))

        conn.commit()

    @staticmethod
    def getOuterNode(innerNode, ontology):
        sqlstr = 'SELECT InnerNode, ontology, outerNode FROM OuterNodesTable'
        for row in cur.execute(sqlstr):
            if innerNode == row[0] and ontology == row[1]:
                return row[2]
        return ''

    @staticmethod
    def addToKeywords(keyword, ontology, layer, URI, cbow, skipgram):
        cur.execute('''INSERT OR IGNORE INTO Keywords (keyword, ontology, layer, URI, CBOW, SkipGram)
                    VALUES ( ?, ?, ?, ?, ?, ? )''', (keyword, ontology, layer, URI, cbow, skipgram))

        conn.commit()

    @staticmethod
    def addToURIsParents(URI, isClass, parents):
        cur.execute('''INSERT OR IGNORE INTO URIsParents (URI, isClass, parents) 
                VALUES ( ?, ?, ? )''', (URI, isClass, parents))
        conn.commit()

    @staticmethod
    def removeDuplicateRows():
        try:
            cur.executescript('''
            DELETE FROM Keywords
            WHERE id NOT IN
            (
                SELECT MIN(id)
                FROM Keywords
                GROUP BY keyword, ontology, layer, URI
            )
            ''')
            conn.commit()
            cur.executescript('''
                    DELETE FROM URIsParents
                    WHERE id NOT IN
                    (
                        SELECT MIN(id)
                        FROM URIsParents
                        GROUP BY URI, isClass, parents
                    )
                    ''')
            conn.commit()
        except:
            print("Error in deleting duplicate rows!! ")

    @staticmethod
    def queryKeywordFromSQL(word, ontology, layer, **kwargs):
        resultForTempQuery = {}
        flag = True
        sqlstr = 'SELECT keyword, ontology, layer, URI, CBOW, SkipGram FROM Keywords'
        for row in cur.execute(sqlstr):
            if word == row[0] and ontology == row[1]:
                if 'tempUse' in kwargs and row[3] is not None and row[4] is not None and row[5] is not None:
                    resultForTempQuery[row[3]] = (row[4], row[5])
                elif 'tempUse' in kwargs and row[3] is None or row[4] is None or row[5] is None:
                    continue
                elif row[3] is not None:
                    queryURIs.append(row[3])
                    queryURIsTuples[row[3]] = (row[4], row[5])
                elif row[3] is None:
                    # keyword exists in database but has no URIs assigned to it
                    return True
                flag = False
        if 'tempUse' in kwargs:
            return resultForTempQuery

        # keyword is not in database
        elif flag:
            return False
        elif not flag:
            return True

    @staticmethod
    def keywordExists(word, ontology, layer):
        sqlstr = 'SELECT keyword, ontology, layer FROM Keywords'
        for row in cur.execute(sqlstr):
            if word == row[0] and row[1] == ontology and row[2] == layer:
                return True
        return False

    @staticmethod
    def readPDFSIntoSQLTable():
        projectPath = os.path.abspath(os.path.dirname(__file__))
        cur.executescript('''
                           create table if not exists PDFTexts (
                                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT unique,   
                                PDF TEXT,
                                PageNumber TEXT,
                                Content TEXT  
                            );
                            ''')
        conn.commit()

        PDFslist = []
        sqlstr = 'SELECT PDF FROM PDFTexts'
        for row in cur.execute(sqlstr):
            PDFslist.append(row[0])

        def addPDFTextToSQLTable(pdfName, pageNum, content):
            cur.execute('''INSERT OR IGNORE INTO PDFTexts (PDF, PageNumber, Content) 
                            VALUES ( ?, ?, ? )''', (pdfName, pageNum, content))
            conn.commit()

        for file in glob.glob( projectPath + "/AllFiles/*.pdf"):
            if file in PDFslist:
                continue
            print("Reading ", file)
            pageNum = 0
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    pageNum = pageNum + 1
                    print("extracting page", pageNum)
                    addPDFTextToSQLTable(file, pageNum, page.extract_text(x_tolerance=0.15, y_tolerance=1).lower())

    @staticmethod
    def readPDFContentsIntoASingleString():
        projectPath = os.path.abspath(os.path.dirname(__file__))

        # PDF contents will be stored in this string
        result = ""
        sqlstr = 'SELECT content FROM PDFTexts'
        for row in cur.execute(sqlstr):
            result += row[0]
        f = open(projectPath + "/AllFiles/text.txt", 'r')
        result += f.read()
        return result
