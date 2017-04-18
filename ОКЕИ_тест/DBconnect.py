import psycopg2
DBSet = "dbname='TestTextToDB' user='ds1' host='localhost' password='1q'"

def checkDBconnect(DB=DBSet):
    """Check connection to DB"""
    try:
        conn = psycopg2.connect(DB)
        print("DB connected, Ok")
    except:
        print("I am unable to connect to the database")
    conn.close()


def createDBTables():
    """Create DB"""
    try:
        conn = psycopg2.connect(DBSet)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE TYPES
               (ID                       SERIAL  NOT NULL,
               TYPESNAME                 TEXT    PRIMARY KEY
               );''')

        cur.execute('''CREATE TABLE SUBTYPE
               (ID                       SERIAL  NOT NULL,
               TypesName                 TEXT    REFERENCES TYPES (TYPESNAME),
               SUBTYPE                   TEXT    NOT NULL,
               TupesName_Subtipe         TEXT    PRIMARY KEY
               );''')

        cur.execute('''CREATE TABLE DATA
               (ID                       SERIAL  NOT NULL,
               TName_Subtipe             TEXT    REFERENCES SUBTYPE (TupesName_Subtipe),
               CODE                      TEXT    PRIMARY KEY,
               UNITNAME                  TEXT    NOT NULL,
               LOCAL_SYMBOL              TEXT,
               INTERNATIONAL_SYMBOL      TEXT,
               LOCAL_ABC_CODE            TEXT,
               INTERNATIONAL_ABC_CODE    TEXT,
               ADDITIONAL_INFORMATION    TEXT
               );''')
        
        print("Tables created successfully \n")
        conn.commit()
        conn.close()
    except:
        print('Table already exist \n')


def insUnitData(u=[['1. МЕЖДУНАРОДНЫЕ ЕДИНИЦЫ ИЗМЕРЕНИЯ, ВКЛЮЧЕННЫЕ В ОКЕИ']]):
    """Units Type record"""
    try:
        conn = psycopg2.connect(DBSet)
        cur = conn.cursor()
        cur.execute("INSERT INTO TYPES (TYPESNAME) VALUES (%s);",(u[0]))
        conn.commit()
        conn.close()
        a=0
        return a
    except psycopg2.IntegrityError:
        print('Types already in DB: ', u[0][0])
        a=1
        return a
        

def insSubTypeData(l=[['1. МЕЖДУНАРОДНЫЕ ЕДИНИЦЫ ИЗМЕРЕНИЯ, ВКЛЮЧЕННЫЕ В ОКЕИ'],
                      ['Единицы длины'],[]]):
    """Units Subtype record"""
    try:
        TupesName_Subtipe = l[0][0]+'_'+l[1][0]
        conn = psycopg2.connect(DBSet)
        cur = conn.cursor()
        cur.execute("""INSERT INTO SUBTYPE (TypesName, SUBTYPE, TupesName_Subtipe) VALUES (%s, %s, %s);""",
                    (l[0][0], l[1][0],TupesName_Subtipe))
        conn.commit()
        conn.close()
        a=0
        return a
    except psycopg2.IntegrityError:
        print('SubTypes already in DB: ', l[1][0])
        print( '             for Type :  ', l[0][0])
        a=1
        return a


def insData(l=[[' 1. МЕЖДУНАРОДНЫЕ ЕДИНИЦЫ ИЗМЕРЕНИЯ, ВКЛЮЧЕННЫЕ В ОКЕИ_ Единицы длины'],
                ['003'], ['Test'], ['мм'], ['mm'], [''], ['ММТ'],[]]):
    """Data record to DB"""
    try:
        conn = psycopg2.connect(DBSet)
        cur = conn.cursor()
        cur.execute("""INSERT INTO DATA (TName_Subtipe, CODE, UNITNAME, LOCAL_SYMBOL, INTERNATIONAL_SYMBOL,
                    LOCAL_ABC_CODE, INTERNATIONAL_ABC_CODE) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                    (l[0][0],l[1][0],l[2][0],l[3][0],l[4][0],l[5][0],l[6][0]))
        conn.commit()
        conn.close()
        a=0
        return a
    except:
        print('Data already in DB for Код  : ', l[1][0])
        a=1
        return a


def readTypeData():
    """Reading Data from DB"""
    conn = psycopg2.connect(DBSet)
    cur = conn.cursor()
    cur.execute("""SELECT CODE, UNITNAME, LOCAL_SYMBOL, INTERNATIONAL_SYMBOL, LOCAL_ABC_CODE,
                INTERNATIONAL_ABC_CODE  from DATA""")
    rows = cur.fetchall()
    for r in rows:
        line = []
        #CODE = r[0]
        #UNITNAME = r[1]
        line = [[r[0]],[r[1]],[r[2]],[r[3]],[r[4]],[r[5]]]
        print(line)
    conn.commit()
    conn.close()



def DropDBTables():
    try:
        conn = psycopg2.connect(DBSet)
        cur = conn.cursor()
        cur.execute("""DROP TABLE DATA, SUBTYPE, TYPES;""")
        conn.commit()
        conn.close()
        print('Tables Dropped successfully')
    except:
        print('Tables already Dropped and dosnt exist')
        #return 1



"""
# Обновление данных --------------------

#Удаление данных -----------------------

#-----------------------------------

"""

