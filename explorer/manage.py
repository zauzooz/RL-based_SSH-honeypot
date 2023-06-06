import os
import sqlite3
import pickle
import shutil
from hashlib import sha256
from TheExplorer import Explorer

"""

"""

def update_database(files_out_path_list: list):

    conn = sqlite3.connect("database/knowlege_base_command.db")
    cursor = conn.cursor()
    TABLE_NAME = "KNOWLEDGE_DB"

    for file_path in files_out_path_list:
        cmd_out = pickle.load(open(file_path,"rb"))
        keys = cmd_out.keys()
        values = cmd_out.values()
        keys_values = list(zip(keys, values))
        for (cmd, out) in keys_values:
            try:
                id = sha256((cmd + out).encode()).hexdigest()
                insert_query = f"INSERT INTO {TABLE_NAME} (id, command, output ) VALUES (?, ?, ?)"
                data = (id, cmd, out)
                cursor.execute(insert_query, data)
                conn.commit()
            except:
                pass
        
    cursor.close()
    conn.close()

def get_files(dir_path):
    files_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            files_list.append(dir_path + "/" + file)
    return files_list

def delete_files(list_path: dict, trash_path: str):
    """
        Move file to trash.
    """
    for file in list_path:
        shutil.move(src=file, dst=trash_path)


def run():
    # get all unknown files name.
    files_path_list = get_files("learner/var/explorer")

    # start Explorer, input is all unknown files name need to process.
    explorer = Explorer(files_path_list)
    explorer.start()

    # update output to the database.
    files_out_path_list = get_files("explorer/var")
    update_database(files_out_path_list)

    # delete unknown files are proccessed.
    delete_files(files_path_list, "learner/var/trash")

    # delete output file
    delete_files(files_out_path_list, "explorer/trash")


if __name__ == "__main__":
    run()