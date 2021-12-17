import sqlite3


conn = sqlite3.connect('URIs.sqlite')
cur = conn.cursor()
cur.executescript('''
        DROP TABLE IF EXISTS URIsParents;
        
        CREATE TABLE URIsParents (
            id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            URI   TEXT,
            isClass TEXT,
            parents TEXT
        );
        ''')


class CreateSQL:
    @staticmethod
    def createTable():
        cur.executescript('''
                DROP TABLE IF EXISTS URIsParents;

                CREATE TABLE URIsParents (
                    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    URI   TEXT,
                    isClass TEXT,
                    parents TEXT
                );
                ''')
        conn.commit()

    @staticmethod
    def addURI(URI, isClass, parents):
        cur.execute('''INSERT INTO URIsParents (URI, isClass, parents)
                VALUES ( ?, ?, ? )''', (URI, isClass, parents))
        conn.commit()
