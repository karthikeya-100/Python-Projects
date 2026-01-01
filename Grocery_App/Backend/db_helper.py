import mysql.connector
from contextlib import contextmanager
import datetime
import calendar


@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "grocery_manager"
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_groceries(month,year):
    with get_db_cursor() as cursor:
        if month !='All':
            cursor.execute(
                '''
                SELECT * FROM groceries
                where MONTH(date_value) = %s and YEAR(date_value) = %s
                '''
            ,(month,year))
            groceries = cursor.fetchall()
            return groceries  # returns list of dictionaries
        else:
            cursor.execute(
                '''
                SELECT * FROM groceries
                where year(date_value) = %s
                '''
            ,(year,))
            groceries = cursor.fetchall()
            return groceries

def insert_grocery(month,year,grocery_item,quantity_value,quantity_unit,place_bought):
    with get_db_cursor(commit = True) as cursor:
        today_day = datetime.date.today().day
        date_obj = datetime.date(year,month,today_day)

        cursor.execute(
            '''
            INSERT INTO groceries (date_value,grocery_item,quantity_value,quantity_unit,place_bought)
            VALUES
            (%s,%s,%s,%s,%s)
            '''
        ,(date_obj,grocery_item,quantity_value,quantity_unit,place_bought))
        return cursor.lastrowid # Assigns row id to newly added row

def delete_grocery(grocery_id):
    with get_db_cursor(commit = True) as cursor:
        cursor.execute(
            '''
            DELETE from groceries 
            where grocery_id = %s
            '''
        ,(grocery_id,))

def handle_is_bought(bought_value,grocery_id):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            '''
            UPDATE groceries 
            set is_bought = %s
            where grocery_id = %s
            '''
        ,(bought_value,grocery_id))


def update_grocery(grocery_id,grocery_item,quantity_value,quantity_unit,place_bought):
    with get_db_cursor(commit = True) as cursor:
        cursor.execute(
            '''
            UPDATE groceries
            set grocery_item = %s,
            quantity_value = %s,
            quantity_unit = %s,
            place_bought = %s
            where grocery_id = %s
            '''
        ,(grocery_item,quantity_value,quantity_unit,place_bought,grocery_id))

