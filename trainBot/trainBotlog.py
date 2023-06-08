import datetime
import os
import logging

def write_log(formatted_datetime: str, msg: str):
    path = "trainBot/log"
    logging.basicConfig(filename=f'trainBot/log/trainBotlog_{formatted_datetime}.log', 
                        level=logging.INFO,
                        format='[%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S:]')
    logging.info(msg=" [trainBot] "+msg)