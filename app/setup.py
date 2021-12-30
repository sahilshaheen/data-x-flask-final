import sqlite3

def create_schema():
    conn = sqlite3.connect('predictions.db')

    print("Opened DB")

    conn.execute("DROP TABLE IF EXISTS results")

    conn.execute("""
    CREATE TABLE results (
        id INTEGER PRIMARY KEY,
        review TEXT NOT NULL,
        prediction TEXT NOT NULL,
        feedback TEXT
    );
    """)

    print("CREATED results")

    conn.close()

    print("Connection closed")

if __name__ == "__main__":
    create_schema()
