import sqlite3


conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()
cur.executescript('''
        DROP TABLE IF EXISTS URIs;
        
        CREATE TABLE URIs (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            URI   TEXT,
            isClass TEXT,
            parents TEXT
        );
        ''')


class CreateSQL:

    @staticmethod
    def addURI(URI, isClass, parents):
        cur.execute('''INSERT INTO URIs (URI, isClass, parents)
                VALUES ( ?, ?, ? )''', (URI, isClass, parents))
        conn.commit()
