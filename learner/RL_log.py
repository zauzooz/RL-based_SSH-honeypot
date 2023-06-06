import datetime
import os
import logging

def write_log(msg:str):
    path = "learner/log/"
    logging.basicConfig(filename='learner/log/log.log', 
                        level=logging.INFO,
                        format='[%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S:]')
    logging.info(msg=msg)