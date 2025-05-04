import psycopg2
import os

DB = {
    "host": os.environ['DB_HOST'],
    "dbname": os.environ['DB_NAME'],
    "user": os.environ['DB_USER'],
    "password": os.environ['DB_PASS']
}

conn = psycopg2.connect(**DB)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        edad INT NOT NULL
    )
""")

conn.commit()
cur.close()
conn.close()

print("Tabla creada o ya existente.")
