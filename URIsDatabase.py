import sqlite3


conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()


class URIsDatabase:
    @staticmethod
    def createKeywordsTable():
        cur.executescript('''
                   create table if not exists Keywords (
                        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
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
                    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    URI   TEXT unique,
                    isClass TEXT,
                    parents TEXT,
                    UNIQUE (URI, isClass, parents) ON CONFLICT IGNORE
                );
                ''')
        conn.commit()

    @staticmethod
    def addToKeywords(keyword, ontology, URI):
        cur.execute('''INSERT or ignore INTO Keywords (keyword, ontology, URI)
                    VALUES ( ?, ?, ? )''', (keyword, ontology, URI))

        conn.commit()

    @staticmethod
    def addToURIsParents(URI, isClass, parents):
        cur.execute('''INSERT OR ignore INTO URIsParents (URI, isClass, parents)
                VALUES ( ?, ?, ? )''', (URI, isClass, parents))
        conn.commit()
