#setup the logging
import logging
import os 
import sys


logging_str="[%(asctime)s]: [%(levelname)s]: [%(name)s]: [%(funcName)s]: [%(lineno)d]: [%(message)s]"

log_dir="logs"
log_filepath=os.path.join(log_dir,"logging.log")
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger=logging.getLogger("datasciencelogger") #name of the logger

