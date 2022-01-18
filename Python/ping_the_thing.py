#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" ping_the_thing.py from weigu.lu """

__version__ = "0.1.0"
__author__ = "Guy WEILER weigu.lu"
__copyright__ = "Copyright 2022, weigu.lu"
#__credits__ = ["Guy WEILER", ]
__license__ = "GPL"
__maintainer__ = "Guy WEILER"
__email__ = "weigu@weigu.lu"
__status__ = "Production" # "Prototype", "Development", or "Production"

from time import sleep, time
import datetime as dt
import subprocess as sp
import sys

# Mail address to send the mail to
RECEIVER = 'mymail@address' # changer this !! :)

# add here your Ip addresses and a meaningfull name of the thing
WAIT_BETWEEN_CHECKS = 5 # in minutes

# add here your Ip addresses and a meaningfull name of the thing
IP_DICT =  {'192.168.1.50':'myNAS',
            '192.168.1.99':'myImportantServer',
            '192.168.1.100':'myIoTSensor',
            '192.168.1.101':'myMy',
          }

##############################################################################

def ipcheck(ip_dict):
    """ Ping the IP addresses from the dictionary and return a list
    if they are up or down"""
    ip_up_list = []
    for ip_addr in ip_dict.keys():
        status, _ = sp.getstatusoutput("ping -c1 -w2 " + ip_addr)
        if status == 0:
            ip_up_list.append('up')
        else:
            ip_up_list.append('down')
    return ip_up_list

def send_mail(subject, message):
    """ Send the message string to the RECEIVER mail address. """
    try:
        retcode = sp.call('echo ' + message + '| mail -s ' + subject +
                          ' ' + RECEIVER, shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Mail was sent! Child returned", retcode, file=sys.stderr)
    except OSError as error:
        print("Error sending mail: Execution failed:", error, file=sys.stderr)

def send_warning_mail(res_dict, mail_flag_list):
    """ Cook the mail. """
    key_list = list(res_dict.keys())
    val_list = list(res_dict.values())
    for i, _ in enumerate(val_list):
        if val_list[i] == 'down':
            if mail_flag_list[i] != 'true':
                subject = 'WARNING_Mail'
                message =  key_list[i] + ' is down! '
                print(message, end = '')
                send_mail(subject, message)
                mail_flag_list[i] = 'true'
    return mail_flag_list

def create_mail_flag_list():
    """ This list is needed to make shure a warning mail
        is only sent once a day"""
    mail_flag_list = []
    key_list = list(IP_DICT.keys())
    for _ in key_list:
        mail_flag_list.append('false')
    return mail_flag_list

##############################################################################

def main():
    """ main """
    print("\"ping_the_thing.py\" started at ",end='')
    print(dt.datetime.now().isoformat('T', 'seconds'))
    mail_flag_list = create_mail_flag_list()

    while True:
        now_time = dt.datetime.now().time()
        if dt.time(0,0,0) <= now_time <= dt.time(0,0,5):
            mail_flag_list = create_mail_flag_list()
            sleep(5)
        now_sec = time() # in seconds
        if int(now_sec%(60*WAIT_BETWEEN_CHECKS)) == 0:
            ip_up_list = ipcheck(IP_DICT)
            res_dict = dict(zip(IP_DICT.values(), ip_up_list))
            mail_flag_list = send_warning_mail(res_dict, mail_flag_list)
            print('!',end = '')
        sleep(1)

##############################################################################

if __name__ == '__main__':
    main()
