import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        home_team TEXT NOT NULL,
        away_team TEXT NOT NULL,
        home_score INTEGER,
        away_score INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS standings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT NOT NULL,
        game INTEGER,
        win INTEGER,
        draw INTEGER,
        lose INTEGER,
        gd INTEGER,
        point INTEGER)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS gamenum(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gamenum INTEGER)
''')

teams = ['김민규', '김환희', '노우찬', '박세중', '변상훈', '심이루', '염도현']

for team in teams:
    cursor.execute('''
        INSERT INTO standings (team, game, win, draw, lose, gd, point)
        VALUES (?, 0, 0, 0, 0, 0, 0)
    ''', (team,))

cursor.execute('''
    INSERT INTO gamenum (gamenum)
    VALUES (0)
''')

conn.commit()
print("table created")