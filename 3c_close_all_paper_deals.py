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
from datetime import date
from pprint import pprint



my_action = ""
arguments = len(sys.argv) - 1
if arguments > 0:
    my_action = sys.argv[1]

if my_action == "--help":
    print()
    print("Usage: ./3c_close_all_paper_deals.sh [cancel|panic_sell]")
    print()
    print("arguments:")
    print("    cancel,        cancel all paper deals, leave them in the current asset")
    print("    panic_sell,    sell all paper deals at market price")
    print()
    sys.exit()


if str(my_action) == "cancel" or str(my_action) == "panic_sell":
    my_nothing = "yeay"
else:
    print("Expected argument: cancel / panic_sell")
    print("Specify if I should cancel or panic_sell")
    sys.exit()
    


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

# change to paper account requires api with account write access
# real or paper account is set on global account settings, so manually changing
# this in the 3c web console makes the setting for this script also
error, mode = p3cw.request(
    entity='users',
    action='change_mode',
    payload={
        "mode": 'paper'
    }
)

# info about accounts
error, accounts = p3cw.request(
    entity='accounts',
    action=''
)

grandtotal_bot_sum = 0
grandtotal_bot_closed_sum = 0
grandtotal_bot_reserved_sum = 0

for account in accounts:
    print()
    print('##########################################################################################')
    print()
    print("AccountID: " + str(account['id']) + " # Account Name: " + str(account['name']) + " # Account USD amount: " + str(format(float(account['usd_amount']), '.2f')))

    # fetch deals
    error, deals = p3cw.request(
        entity='deals',
        action='',
        payload={
            "account_id": str(account['id']),
            "limit": 300
        }
    )

    deals_sorted = sorted(deals, key=lambda botname: botname['bot_name'])
    prev_botname = ""
    this_bot_sum = 0
    this_bot_closed_sum = 0
    this_bot_reserved_sum = 0
    
    for deal in deals_sorted:
        if deal['finished?'] == False:
            print("ID: " + str(deal['id']) + " # Start: " + str(deal['created_at']) + " # Stop: " + str(deal['closed_at']), end = '')
            try:
                erroronclose, dealtoclose = p3cw.request(
                    entity='deals',
                    action=str(my_action),
                    action_id=str(deal['id'])
                )
                if dealtoclose['finished?'] == True:
                    print(" # closed_with: " + str(my_action))
            except:
                print(" # ERROR: " + erroronclose['msg'])

            #pprint(dealtoclose)
            #print("------------")
            #pprint(erroronclose)
