import datetime
import os
import logging

def write_log(msg:str):
    path = "trainBot/log"
    logging.basicConfig(filename='trainBot/log/trainBotlog.log', 
                        level=logging.INFO,
                        format='[%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S:]')
    logging.info(msg=" [trainBot] "+msg)