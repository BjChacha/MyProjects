import time

def logging_output(message):
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {message}')

def logging_to_file(filename, message):
    with open(filename, mode='a', encoding='utf-8') as log:
        log.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] {message}\n')