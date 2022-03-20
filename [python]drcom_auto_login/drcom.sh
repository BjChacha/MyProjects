#! /bin/bash

account=381393
password=136135

while true;
    do
        ping -c 3 baidu.com > /dev/null
        if [ $? -eq 0 ]; then
            echo [`date +"%Y-%m-%d %H:%M:%S"`] Device is online. | tee -a drcom.log
        else
            status=0
            while [[ "$status" != "1" ]];
                do
                    echo [`date +"%Y-%m-%d %H:%M:%S"`] Device is offline. Try to reconnecting... | tee -a drcom.log
                    ip=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v 192.168.1.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
                    wget "http://172.30.255.42:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C$account&user_password=$password&wlan_user_ip=$ip&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=zh-cn&v=9407&lang=zh" -q -O login.log
                    info=`cat login.log | grep -Eo ".result..\d"`
                    status=${info:9}
                    if [ "$status" == "1" ]; then
                        echo [`date +"%Y-%m-%d %H:%M:%S"`] Login success. | tee -a drcom.log
                    else
                        echo [`date +"%Y-%m-%d %H:%M:%S"`] Login failed. Try again after 15s... | tee -a drcom.log
                        sleep 15s
                    fi
                done
        fi
        sleep 300s
    done
