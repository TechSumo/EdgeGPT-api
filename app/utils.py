import sqlite3
import json


def create_db_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def json_to_products_list(json_file: str) -> list:

    with open(json_file) as products_file:
        file_contents = products_file.read()

    return json.loads(file_contents)


def create_product(db_connection, product):
    """
    Create a new product into the product table
    :param db_connection:
    :param product:
    :return: product id
    """
    sql = ''' INSERT INTO products(sku,product_name,product_manufacturer)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid
