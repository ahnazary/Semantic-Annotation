import sqlite3

conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()


class KeywordsSQL:
    @staticmethod
    def createTable():
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
    def queryTable():
        sqlstr = 'SELECT keyword, ontology FROM URIsParents'
        for row in cur.execute(sqlstr):
            print(str(row[0]), row[1])

        conn.commit()

    @staticmethod
    def addKeyword(keyword, ontology, URI):
        cur.execute('''INSERT or ignore INTO Keywords (keyword, ontology, URI)
                VALUES ( ?, ?, ? )''', (keyword, ontology, URI))

        conn.commit()
