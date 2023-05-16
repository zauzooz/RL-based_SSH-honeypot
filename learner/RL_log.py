import datetime
import os


def writelog(msg: str):
    today = datetime.datetime.today()
    day_month_year = f"{today.day}-{today.month}-{today.year}"
    filename = f"log/{day_month_year}.txt"
    if os.path.isfile(filename) == False:
        with open(f"{filename}", "w") as f:
            pass
    f = open(filename, "a")
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d-%m-%Y_%H-%M-%S-%f")
    f.write(f"[{formatted_date}] {msg}\n")
    f.close()
