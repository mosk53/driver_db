import logging as log
import logging.handlers as handlers
import time

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[handlers.RotatingFileHandler('log.log', maxBytes=1, backupCount=5)])

def main():
    while True:
        time.sleep(1)
        log.info("A Sample Log Statement")
        log.info("A Sample Log Statement")
 

main()