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



   # create forms annd sql_connecttion files. Make responsive button "Update" and Update rows: Review, Rating in Database