import os
from TheExplorer import Explorer

"""

"""

def delete_unknown_command(file_names_list: list):
    print("delete_unknown_command exec.")

def update_database():
    print("update_database exec.")

def get_files(dir_path):
    files_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            files_list.append(dir_path + "/" + file)
    return files_list

def run():
    # get all unknown files name.
    files_path_list = get_files("learner/var/explorer")

    # start Explorer, input is all unknown files name need to process.
    explorer = Explorer(files_path_list)
    explorer.start()

    # update output to the database.
    update_database()

    # delete unknown files are proccessed.
    delete_unknown_command(files_path_list)

if __name__ == "__main__":
    run()