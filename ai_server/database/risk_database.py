from database import database

def init() -> None:
    database.open()
    database.execute_non_query("""
        CREATE TABLE IF NOT EXISTS Risk (
            id INTEGER PRIMARY KEY,
            at_risk INTEGER NOT NULL,
            complete INTEGER NOT NULL
        );
    """)

def has(id: int) -> bool:
    result = database.execute_query("SELECT COUNT(*) FROM Risk WHERE id=?", (id,))
    count = int(result[0][0])
    return count != 0

def completed(id: int) -> bool:
    result = database.execute_query("SELECT COUNT(*) FROM Risk WHERE id=? AND complete=1", (id,))
    count = int(result[0][0])
    return count != 0

def at_risk(id: int) -> tuple:
    result = database.execute_query("SELECT at_risk,complete FROM Risk WHERE id=? AND at_risk=1 AND complete=1", (id,))
    try:
        at_risk = int(result[0][0]) == 1
        complete = int(result[0][1]) == 1
        return at_risk, complete
    except:
        return 0, 0

def start(id: int) -> None:
    database.execute_commit("INSERT INTO Risk(id, at_risk, complete) VALUES(?, 0, 0)", (id))

def end(id: int, at_risk: int) -> None:
    database.execute_commit("UPDATE Risk SET at_risk=?,complete=1 WHERE id=?", (at_risk, id))
