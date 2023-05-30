from TheExplorer import Explorer
"""

"""

def delete_unknown_command(file_names_list: list):
    pass

def update_database():
    pass

def get_files():
    files_list = []

    return files_list

def run():
    # get all unknown files name.
    file_names_list = get_files()

    # start Explorer, input is all unknown files name need to process.
    explorer = Explorer(file_names_list)
    explorer.start()

    # update output to the database.
    update_database()

    # delete unknown files are proccessed.
    delete_unknown_command(file_names_list)

if __name__ == "__main__":
    run()