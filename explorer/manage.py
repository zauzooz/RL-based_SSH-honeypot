import os
import sqlite3
import pickle
import shutil
from hashlib import sha256
from TheExplorer import Explorer
from datetime import datetime
from explorer_log import write_log

"""

"""

# Get the current datetime
now = datetime.now()

# Format the datetime as "d-m-y_h-m-s-ms"
formatted_datetime = now.strftime("%d-%m-%y_%H-%M-%S-%f")

def percent_match(str1: str, str2: str) -> float:

    def format_string(input_str):
        # Split the input string by whitespace into a list of words
        words = input_str.split()

        # Join the words with a single space in between
        formatted_str = " ".join(words)

        return formatted_str

    if str1 == str2:
        return 1

    # format string to 1 space between 2 words.
    str1 = format_string(str1)
    str2 = format_string(str2)

    # help 2 string that match
    while len(str1) > len(str2):
        str2 += " "
    while len(str2) > len(str1):
        str1 += " "
    
    match_count = sum(c1 == c2 for c1, c2 in zip(str1, str2))
    percentage = match_count / len(str1)
    return percentage

def update_database(files_out_path_list: list):

    conn = sqlite3.connect("database/knowlege_base_command.db")
    cursor = conn.cursor()
    TABLE_NAME = "KNOWLEDGE_DB"

    for file_path in files_out_path_list:
        write_log(formatted_datetime, f"[update database] File path process: {file_path}")
        cmd_out = pickle.load(open(file_path,"rb"))
        keys = cmd_out.keys()
        values = cmd_out.values()
        keys_values = list(zip(keys, values))
        for (cmd, out) in keys_values:
            try:
                # check command is in database.
                check_query = f"SELECT * FROM {TABLE_NAME} WHERE command = '{cmd}'"
                write_log(formatted_datetime, f"[update database] Checking Query: {check_query}")
                cursor.execute(check_query)
                results = cursor.fetchall()

                n_results = len(results)
                if n_results > 0:
                    row = results[0]
                    write_log(formatted_datetime, f"[update database] Query result: {row}")
                    e = percent_match(row, out)
                    if e > 0.7:
                        write_log(formatted_datetime, f"[update database] Because percentant match is larger than 0.7, don't update this command into database.")
                        continue
                    else:
                        write_log(formatted_datetime, f"[update database] Because percentant match is smaller than 0.7, update this command into database.")
                
                id = sha256((cmd + out).encode()).hexdigest()
                insert_query = f"INSERT INTO {TABLE_NAME} (id, command, output ) VALUES (?, ?, ?)"
                data = (id, cmd, out)
                cursor.execute(insert_query, data)
                conn.commit()
            except e:
                write_log(formatted_datetime, f"[update database] Error: {e}.")
        
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
    write_log(formatted_datetime, f"[explorer] Get file paths: {files_path_list}")

    # start Explorer, input is all unknown files name need to process.
    write_log(formatted_datetime, f"[explorer] Explorer start!!!")
    explorer = Explorer(files_path_list)
    explorer.start()

    # update output to the database.
    write_log(formatted_datetime, f"[explorer] Update database Start")
    files_out_path_list = get_files("explorer/var")
    update_database(files_out_path_list)

    # delete unknown files are proccessed.
    delete_files(files_path_list, "learner/var/trash")
    write_log(formatted_datetime, f"[explorer] Move unknown file to trash.")

    # delete output file
    delete_files(files_out_path_list, "explorer/trash")
    write_log(formatted_datetime, f"[explorer] Move cmd-output file to trash.")


if __name__ == "__main__":
    run()