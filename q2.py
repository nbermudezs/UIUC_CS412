from itertools import combinations
import csv
import mysql.connector

"""
Database stuff.
"""
DB_NAME = 'cs412_hw2'

cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost')
"""
Copied from https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
"""
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

"""
Developed by Nestor Bermudez
"""
def set_or_create_db(cursor):
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

def recreate_table(cursor):
    try:
        cursor.execute(
            "DROP TABLE q2")
    except mysql.connector.Error as err:
        pass

    try:
        cursor.execute("""
            CREATE TABLE `q2` (
            `id` int(11) NOT NULL,
            `state` varchar(45) DEFAULT NULL,
            `city` varchar(45) DEFAULT NULL,
            `category` varchar(45) DEFAULT NULL,
            `price` varchar(45) DEFAULT NULL,
            `rating` decimal(5,0) DEFAULT NULL,
            PRIMARY KEY (`id`)
            )""")
    except mysql.connector.Error as error:
        print('Error creating table', error)
"""
End of DB stuff
"""

DIMENSIONS = [ 'id', 'state', 'city', 'category', 'price', 'rating' ]

class Q2DataCube:
    def __init__(self):
        self._dimension_count = len(DIMENSIONS)

    def generate(self):
        return self

    def k_cuboid_dimensions(self, k):
        return combinations(self._dimensions, k)

def load_into_mysql(filepath):
    raw_data = open(filepath, 'rb')
    transactions = csv.DictReader(raw_data, delimiter = ',', fieldnames = DIMENSIONS)

    try:
        cursor = cnx.cursor()
        set_or_create_db(cursor)
        recreate_table(cursor)
        add_record = ("INSERT INTO q2 "
               "(id, state, city, category, rating, price) "
               "VALUES (%(id)s, %(state)s, %(city)s, %(category)s, %(rating)s, %(price)s)")
        for record in transactions:
            cursor.execute(add_record, record)
        cnx.commit()
        print('Records imported into MySQL DB[ name = {0}, table = {1} ]'.format(DB_NAME, 'q2'))
    finally:
        cursor.close()

def generate_data_cube(filepath):
    return Q2DataCube().generate()

if __name__ == '__main__':
    filepath = 'hw2data/Q2data.csv'
    load_into_mysql(filepath)

    cube = generate_data_cube(filepath)

    cnx.close()
