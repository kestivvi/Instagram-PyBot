import sqlite3
from sqlite3 import Error
from pathlib import Path
from tools import config


class ACTION:
    LIKE = 0
    COMMENT = 1
    FOLLOW = 2
    UNFOLLOW = 3
    ERROR = 4


def get_db_path():
    return Path(config.data.data_folder) / "sqlite.db"


def check_db():
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        conn.execute('''CREATE TABLE IF NOT EXISTS user_action
                        (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            date INT NOT NULL,
                            type BYTE NOT NULL
                        )
                    ''')
        conn.execute('''CREATE TABLE IF NOT EXISTS error
                        (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            date INT NOT NULL,
                            message TEXT
                        )
                    ''')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def insert(type: ACTION, message: str = ""):
    check_db()
    conn = sqlite3.connect(get_db_path())
    if type == ACTION.ERROR:
        conn.execute(f'''INSERT INTO error (date, message) VALUES (datetime('now'), "{message}")''');
    else:
        conn.execute(f'''INSERT INTO user_action (date, type) VALUES (datetime('now'), {type})''');
    conn.commit()
    conn.close()


def how_many(type: ACTION, time: int, time_type: str = "Hour") -> int:
    check_db()
    conn = sqlite3.connect(get_db_path())
    if type == ACTION.ERROR:
        cursor = conn.execute(f'''SELECT count(*) FROM error WHERE datetime(date) >= datetime('now', '-{time} {time_type}')''')
    else:
        cursor = conn.execute(f'''SELECT count(*) FROM user_action WHERE datetime(date) >= datetime('now', '-{time} {time_type}') AND type = {type}''')
    result = [row[0] for row in cursor][0]
    conn.close()
    return result


def db2csv():
    import pandas as pd
    conn = sqlite3.connect(get_db_path(), isolation_level=None,
                           detect_types=sqlite3.PARSE_COLNAMES)
    db_df = pd.read_sql_query("SELECT * FROM user_action", conn)
    db_df.to_csv(Path(config.data.data_folder) / 'user_action.csv', index=False)
    db_df = pd.read_sql_query("SELECT * FROM error", conn)
    db_df.to_csv(Path(config.data.data_folder) / 'error.csv', index=False)
    conn.close()

