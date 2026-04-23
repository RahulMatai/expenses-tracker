import sqlite3
from decimal import Decimal
from pathlib import Path #handling paths
from typing import Optional #for hints 

DB_path = Path("expenses.db") #sql path (file path)

def get_connection():
    conn = sqlite3.connect(DB_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id       TEXT NOT NULL UNIQUE,
            amount_paise    INTEGER NOT NULL,
            category        TEXT NOT NULL,
            description     TEXT NOT NULL DEFAULT '',
            date            TEXT NOT NULL,
            created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
        )
    """)
    conn.commit()
    conn.close()

def create_expense(client_id, amount, category, description, date):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category.strip():
        raise ValueError("Category is required.")
    if not date:
        raise ValueError("Date is required.")
    
    amount_paise = int(Decimal(str(amount)) * 100) #safe convertion for paisa
    
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO expenses (client_id, amount_paise, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        """, (client_id, amount_paise, category, description, date))
        conn.commit()
    except sqlite3.IntegrityError: #duplicate entry Ignored
        pass  # duplicate client_id — safe to ignore
    finally:
        conn.close()

def get_expenses(category=None, sort_by_date_desc=True):
    conn = get_connection()
    
    query = "SELECT * FROM expenses"
    params = []
    
    if category and category != "All": # if all we skip where clause  saving potensial bandwidth
        query += " WHERE category = ?"
        params.append(category)
    
    if sort_by_date_desc:
        query += " ORDER BY date DESC"
    else:
        query += " ORDER BY date ASC"
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    result = []
    for row in rows:
        d = dict(row)
        d["amount_rupees"] = Decimal(d["amount_paise"]) / 100 #added back as Decimal for display
        result.append(d)
    
    return result