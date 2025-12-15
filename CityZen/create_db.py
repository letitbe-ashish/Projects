import sqlite3

# Connection to database 
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Creating issues table
cursor.execute('''
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    pincode TEXT,
    email TEXT,
    phone TEXT,
    issue_type TEXT,
    description TEXT,
    image TEXT,  -- This will store the image filename or path
    status TEXT DEFAULT 'Pending',
    vote INTEGER DEFAULT 0,
    assign_to TEXT,
    created_at TEXT
)
''')

#  Create votes table for one vote per session per issue
cursor.execute('''
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issue_id INTEGER,
    user_session TEXT,
    UNIQUE(issue_id, user_session)
)
''')

# Create login_info table
cursor.execute('''
CREATE TABLE IF NOT EXISTS login_info (
    user_name TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
    
)
''')

# Create admin_login table
cursor.execute('''
CREATE TABLE IF NOT EXISTS admin_login (
    adm_username TEXT PRIMARY KEY,
    adm_password TEXT NOT NULL
)
''')

# Create general_queries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS general_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    answer TEXT DEFAULT 'Pending'
)
''')



conn.commit()
conn.close()
print("Database and all tables created.")
