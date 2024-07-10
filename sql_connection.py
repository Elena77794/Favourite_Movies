import mysql.connector

__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(user='root',
                                     host='localhost',
                                     port="3306",
                                        database='Top_Movie_Web')
        return __cnx



