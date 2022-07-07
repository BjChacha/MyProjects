from login import drcom_login_dormitory, drcom_login_lab
from log import logging_output, logging_to_file
from util import check_online, get_account

import time

# query interval: second
CD_SECOND = 60
# enale logging output
DEBUG = True
# file to logging
LOG_FILE = 'log.txt'

def main():

    debug = DEBUG
    account, password = get_account()

    while True:
        try:
            if check_online():
                if debug:
                    logging_output('Device online.')
                    logging_to_file('log.txt', 'Device online')
            else:
                if debug:
                    logging_output('Device offling, reconnecting...')
                    logging_to_file('log.txt', 'Device offling, reconnecting...')
                try:
                    status = drcom_login_dormitory(account, password)
                    if debug:
                        if status == 'OK':
                            logging_output("Login success!")
                        else:
                            logging_output('Login failed, try again...')
                except Exception:
                    if debug:
                        logging_output('Login process failed. Debug is required.')
        except Exception:
            if debug:
                logging_output('Runing script failed. Debug is required.')

        time.sleep(CD_SECOND)

if __name__ == '__main__':
    main()