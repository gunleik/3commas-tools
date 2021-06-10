#################################################################
#
#   3commas bot stats
#   giving a better overview of your deals in 3commas
#
#   https://github.com/gunleik/3commas-tools
#
#   @gunleik
#
#################################################################



import time
import sys
import os

from py3cw.request import Py3CW
from datetime import datetime
#from pprint import pprint


log_min      = False
hide_futures = False

arguments = len(sys.argv) - 1
if arguments > 0:
    for this_argument in sys.argv:
        if this_argument == "--help":
            print()
            print("Usage: ./3c_account_stats.sh")
            print()
            print("optional arguments:")
            print("    minimal,        printout better for piping to logfile")
            print("    hidefutures,    hide accounts with futures in the name")
            print()
            sys.exit()
        if this_argument == "minimal":
            log_min = True
        if this_argument == "hidefutures":
            hide_futures = True

# initiate API with key/secret from os env
p3cw = Py3CW(
    key=os.environ.get('threecommas_key').rstrip(),
    secret=os.environ.get('threecommas_secret').rstrip(),
    request_options={
        'request_timeout': 10,
        'nr_of_retries': 1,
        'retry_status_codes': [502]
    }
)

error, mode = p3cw.request(
    entity='users',
    action='change_mode',
    payload={
        "mode": 'real'
    }
)

# info about accounts
error, accounts = p3cw.request(
    entity='accounts',
    action=''
)

total_usd_value = 0

if log_min == False:
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))

for account in accounts:
    if hide_futures == True and "utures" in str(account['name']):
        hidethis = ""
    else:
        if log_min == True:
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"), end = ' # ')
        print("AccountID: " + str(account['id']), end = ' # ')
        print('Name: "' + str(account['name']), end = '" # ')
        print("USD_value: " + str(format(float(account['usd_amount']), '.2f')))
        total_usd_value = total_usd_value + float(account['usd_amount'])

if log_min == False:
    print("-------------------------------------------------")
    now = datetime.now()

if log_min == True:
    print(now.strftime("%Y-%m-%d %H:%M:%S"), end = ' # ')

print("Total_USD_value: " + str(format(float(total_usd_value), '.2f')))

if log_min == False:
    print("=================================================")
