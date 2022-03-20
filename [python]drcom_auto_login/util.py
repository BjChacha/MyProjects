from ipaddress import ip_address
import os
# import re
import socket
import configparser

# def get_ip_address():

#     ipconfig = os.popen('chcp 65001&&ipconfig').read()
#     ip_address = re.findall('IPv4 Address.*?: (.*?)\n', ipconfig)[0]

#     return ip_address

def get_ip_address():

    ip_address = ""
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8',80))
        ip_address = s.getsockname()[0]

    return ip_address

def check_online():
    
    status = os.system("ping baidu.com -n 1 -w 2")
    return status == 0

def get_account():
    account, password = '', ''
    try:
        parser = configparser.ConfigParser()
        parser.read("account.ini")
        account_info = parser.items('account')
        account, password = account_info[0][1], account_info[1][1]
    except:
        print("Read account infomartion failed. Please config your account info in account.ini file.")
    return account, password