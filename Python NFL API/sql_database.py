import sqlite3

class Create_db():
    def __init__(self):
        try:
            self.conn = sqlite3.connect("nfl_data.db")
            self.c = self.conn.cursor()
        except sqlite3.OperationalError: #pass if table already exists
            pass

    def create_table(self, columns):
        self.c.execute(f"""
            CREATE TABLE [IF NOT EXISTS] play_data (
            {columns[0]} INT PRIMARY KEY,
            {columns[1]} INT,
            {columns[2]} STR, 
            {columns[3]} INT,
            {columns[4]} INT,
            
            
        """, columns)
        self.conn.commit()
        self.conn.close()

    def insert_data(self, data):
        self.c.execute("INSERT INTO nfl_data VALUES (?, ?, ?)", data)
        self.conn.commit()
        self.conn.close()
