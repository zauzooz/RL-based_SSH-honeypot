import logging

def write_log(formatted_datetime: str, msg: str):
    path = "explorer/log"
    logging.basicConfig(filename=f'explorer/log/explorer_{formatted_datetime}.log', 
                        level=logging.INFO,
                        format='[%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S:]')
    logging.info(msg=msg)