Q_TABLE = {"exit": [0.0]}

COMMAND_DATABASE = {
    "ls": ["list file and directory."],
    "pwd": ["current directory."],
    "exit": [""],
}


def get_output_in_database(key: str):
    if key in COMMAND_DATABASE.keys():
        return COMMAND_DATABASE[key]
    return "unknown"
