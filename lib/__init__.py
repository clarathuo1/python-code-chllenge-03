import sqlite3

CONN = sqlite3.connect('concerts_database.db')
CURSOR = CONN.cursor()