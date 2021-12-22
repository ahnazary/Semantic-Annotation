import sqlite3

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
    def removeDuplicateRows(tableName):
        cur.executescript('''
          DELETE
          FROM ''' + "Keywords " +
                          '''WHERE NOT EXISTS
          (
          select 1 from 
          (
          select min(id) as id, keyword, ontology, URI
          From Keywords A
          Group by keyword, ontology, URI
          ) B
          Where B.id = Keywords.id
          AND   B.keyword = Keywords.keyword
          AND   B.ontology = Keywords.ontology
          AND   B.URI = Keywords.URI 
          )
        ''')
        conn.commit()
