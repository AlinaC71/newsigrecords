from flask import Flask
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Andr66a1995',
    'database': 'mysigrec',
}



def execute_query(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows
















