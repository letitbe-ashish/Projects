import sqlite3

def init_db():
    conn = sqlite3.connect('cityzen.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending',
            votes TEXT NOT NULL
            
        )
    ''')
    conn.commit()
    conn.close()
