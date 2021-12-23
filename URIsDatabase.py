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
    def addToKeywords(keyword, ontology, URI):
        cur.execute('''INSERT OR IGNORE INTO Keywords (keyword, ontology, URI)
                    VALUES ( ?, ?, ? )''', (keyword, ontology, URI))

        conn.commit()

    @staticmethod
    def addToURIsParents(URI, isClass, parents):
        cur.execute('''INSERT OR IGNORE INTO URIsParents (URI, isClass, parents) 
                VALUES ( ?, ?, ? )''', (URI, isClass, parents))
        conn.commit()

    @staticmethod
    def removeDuplicateRows():
        cur.executescript('''
        DELETE FROM Keywords
        WHERE id NOT IN
        (
            SELECT MIN(id)
            FROM Keywords
            GROUP BY keyword, ontology, URI
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

    @staticmethod
    def keywordExists(word):
        flag = True
        sqlstr = 'SELECT keyword, URI FROM Keywords'
        for row in cur.execute(sqlstr):
            if word == row[0]:
                if row[1] is not None:
                    print("keyword exists", row[1].split(","))
                    for URI in row[1].split(","):
                        queryURIs.append(URI)
                        tempTuple = (1, 1)
                        queryURIsTuples[URI] = tempTuple
                else:
                    print("keyword exists", row[1])
                flag = False
        if flag:
            print("Keyword does not exist")
            return False
        if not flag:
            return True



