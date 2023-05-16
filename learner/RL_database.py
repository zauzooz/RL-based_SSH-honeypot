import os
import sqlite3
from hashlib import sha256

Q_TABLE = {"exit": [0.0]}


class CommandKnowledgeBase:
    def __init__(self, dbPath: str = "database/knowlege_base_command.db"):
        self.conn = sqlite3.connect(dbPath)
        self.table_name = "KNOWLEDGE_DB"
        self.columns = ["id", "command", "output"]  # ID <- SHA256(COMMAND+OUTPUT)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                {self.columns[0]} TEXT PRIMARY KEY ,
                {self.columns[1]} TEXT,
                {self.columns[2]} TEXT
                )"""
        )

    def add_new(self, command: str, output: str):
        id: str = sha256((command + output).encode()).hexdigest()
        insert_query = f"INSERT INTO {self.table_name} ({self.columns[0]}, {self.columns[1]}, {self.columns[2]}) VALUES (?, ?, ?)"
        data = (id, command, output)

        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def is_command_in_db(self, command: str):
        # execute SELECT statement to check if command is in database
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {self.columns[1]} = ?"
        self.cursor.execute(query, (command,))
        result = self.cursor.fetchone()[0]
        return result > 0

    def get_output_by_cmd(self, cmd: str):
        # trả về danh sách các OUTPUT có cmd tương ứng.
        select_query = f"SELECT {self.columns[2]} FROM {self.table_name} WHERE {self.columns[1]} = ?"
        self.cursor.execute(select_query, (cmd,))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            return [row[0] for row in rows]
        return ["nnt@nnt:~$"]

    def close(self):
        self.cursor.close()
        self.conn.close()


# COMMAND_DATABASE = {}

# if __name__ == "__main__":
#     db = CommandKnowledgeBase()
#     cmd = "ls"
#     output = """LICENSE  README  README.md  lib  peda.py  python23-compatibility.md\nnnt@nnt:~/peda$"""
#     db.add_new(command=cmd, output=output)
#     cmd = "nnt@nnt:~$ cd peda/"
#     output = "nnt@nnt:~/peda$"
#     db.add_new(command=cmd, output=output)
#     db.close()
