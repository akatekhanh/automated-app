import sqlite3

def create_connection():
    return sqlite3.connect('negotiation_results.db')

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS negotiation_results')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS negotiation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            a1_utility REAL,
            a2_utility REAL,
            a1_offers TEXT,
            a2_offers TEXT,
            result TEXT,
            winner TEXT,
            a1_steps INTEGER,
            a2_steps INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(conn, a1_steps, a2_steps, a1_utility, a2_utility, a1_offers, a2_offers, result, winner):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO negotiation_results (a1_steps, a2_steps, a1_utility, a2_utility, a1_offers, a2_offers, result, winner)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (a1_steps, a2_steps, a1_utility, a2_utility, a1_offers, a2_offers, result, winner))
    conn.commit()
    conn.close()