import sqlite3

from FeatureVector import queryURIs, queryURIsTuples

conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()


class URIsDatabase:
    @staticmethod
    def createKeywordsTable():
        cur.executescript('''
                
                   create table if not exists Keywords (
                        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT unique,
                        keyword TEXT,
                        ontology TEXT,
                        layer TEXT,
                        URI TEXT,
                        UNIQUE (keyword, ontology, URI)
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
    def addToKeywords(keyword, ontology, layer, URI):
        cur.execute('''INSERT OR IGNORE INTO Keywords (keyword, ontology, layer, URI)
                    VALUES ( ?, ?, ?, ? )''', (keyword, ontology, layer, URI))

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
    def queryKeywordFromSQL(word, ontology, layer):
        flag = True
        sqlstr = 'SELECT keyword, ontology, layer, URI FROM Keywords'
        for row in cur.execute(sqlstr):
            if word == row[0] and ontology == row[1] and layer == row[2]:
                if row[3] is not None:
                    # print("keyword exists", row[3].split(","))
                    for URI in row[3].split(","):
                        queryURIs.append(URI)
                        tempTuple = (1, 1)
                        queryURIsTuples[URI] = tempTuple
                else:
                    # print("keyword exists in database but has no URIs assigned to it", row[3])
                    return True
                flag = False
        if flag:
            print("Keyword does not exist in the database")
            return False
        if not flag:
            return True

    @staticmethod
    def keywordExists(word, ontlogy, layer):
        sqlstr = 'SELECT keyword, ontology, layer FROM Keywords'
        for row in cur.execute(sqlstr):
            if word == row[0] and row[1] == ontlogy and row[2] == layer:
                return True
        return False



