def clear_explore_states():
    import os

    # Directory path
    directory = '/home/honeypot/RL-based_SSH-honeypot/learner/var/rl/explore_states'

    # Change to the specified directory
    os.chdir(directory)

    # Get the name of the Python script
    script_name = 'clear.py'

    # Get a list of all files in the directory
    files = os.listdir()

    # Sort files by modification time in reverse order
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(x), reverse=False)

    # Loop through the files and delete all except the specified Python script and the last file
    for file in sorted_files[:-1]:
        if file != script_name:
            os.remove(file)
            print(f"Deleted file: {file}")

def clear_q_table():
    import os

    # Directory path
    directory = '/home/honeypot/RL-based_SSH-honeypot/learner/var/rl/q-table'

    # Change to the specified directory
    os.chdir(directory)

    # Get the name of the Python script
    script_name = 'clear.py'

    # Get a list of all files in the directory
    files = os.listdir()

    # Sort files by modification time in reverse order
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(x), reverse=False)

    # Loop through the files and delete all except the specified Python script and the last file
    for file in sorted_files[:-1]:
        if file != script_name:
            os.remove(file)
            print(f"Deleted file: {file}")

def clear_explorer():
    import os

    # Directory path
    directory = '/home/honeypot/RL-based_SSH-honeypot/learner/var/explorer'

    # Change to the specified directory
    os.chdir(directory)

    # Get a list of all files in the directory
    files = os.listdir()

    # Sort files by modification time in reverse order
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(x), reverse=False)

    # Loop through the files and delete all except the specified Python script and the last file
    for file in sorted_files:
        os.remove(file)
        print(f"Deleted file: {file}")


if __name__ == "__main__":
    clear_q_table()
    clear_explore_states()
    clear_explorer()

