import sqlite3

def init_db():
    conn = sqlite3.connect('sentiment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        sentiment TEXT,
        score REAL,
        emoji TEXT,
        stars INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# Call this once during app startup
init_db()
