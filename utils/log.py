import os
import logging
from utils.settings import settings

def startLogging():
    configPath = os.getenv("HOME") + "/.config/Discline"
    if os.path.exists(configPath):
        logging.basicConfig(filename=configPath + "/discline.log", filemode='w',
                level=logging.INFO)
    else:
        logging.basicConfig(filename="discline.log", filemode='w', level=logging.INFO)

def log(msg, func=logging.info):
    if settings["debug"]:
        func(msg)
