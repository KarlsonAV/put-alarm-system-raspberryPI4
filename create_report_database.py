import sqlite3

def create_alarm_system_table():
    connection = sqlite3.connect('report_database.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alarm_system (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            DATE TEXT,
            image BLOB,
            Faces INTEGER
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_alarm_system_table()
    print("SQLite database and 'alarm_system' table created successfully.")
