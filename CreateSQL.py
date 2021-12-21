import sqlite3


conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()


class CreateSQL:
    @staticmethod
    def createTable():
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
    def addURI(URI, isClass, parents):
        cur.execute('''INSERT OR ignore INTO URIsParents (URI, isClass, parents)
                VALUES ( ?, ?, ? )''', (URI, isClass, parents))
        conn.commit()
