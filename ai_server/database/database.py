import sqlite3

###
### WARNING: This simple framework has not been tested for thread safety!
###

connection = None
cursor = None

def open() -> None:
    global connection, cursor
    if connection is not None:
        return
    connection = sqlite3.connect("fluprint_ai.db", check_same_thread=False)
    cursor = connection.cursor()

def execute_non_query(statement: str, params: tuple = ()) -> None:
    cursor.execute(statement, params)

def execute_query(query: str, params: tuple = ()) -> list:
    result = cursor.execute(query, params)
    return result.fetchall()

def execute_commit(statement: str, params: tuple = ()) -> None:
    cursor.execute(statement, params)
    connection.commit();

def close() -> None:
    connection.close()
