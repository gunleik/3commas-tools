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
#from pprint import pprint




arguments = len(sys.argv) - 1
if arguments > 0:
    me_want = sys.argv[1]
else:
    me_want = "today"

if arguments > 1:
    argument2 = sys.argv[2]
else:
    argument2 = "na"

if me_want == "today" or me_want == "active":
    my_limit = 250
else:
    my_limit = 1000


if me_want == "--help":
    print()
    print("Usage: ./3c_bot_stats.sh [today|active|all|datefilter] [totals]")
    print()
    print("optional arguments:")
    print("    today,    (default) show deals started, ended today or currently running")
    print("    today totals,       todays deals, but don't show individual deals")
    print("    active,             show deals currently running")
    print("    all,                show all deals (limit on 1000 per account)")
    print("    datefilter,         e.g. 2021-05-31 to show deals from specific date")
    print()
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
#error, mode = p3cw.request(
#    entity='users',
#    action='change_mode',
#    payload={
#        "mode": 'paper'
#    }
#)

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
            "limit": my_limit
        }
    )

    deals_sorted = sorted(deals, key=lambda botname: botname['bot_name'])
    prev_botname = ""
    this_bot_sum = 0
    this_bot_closed_sum = 0
    this_bot_reserved_sum = 0
    this_bot_opendeals    = 0
    this_bot_closeddeals  = 0
    show_openclosed = False
    
    for deal in deals_sorted:
        if deal['finished?'] == True:
            this_profitpst = str(deal['final_profit_percentage'])
            this_profitusd = str(format(float(deal['usd_final_profit']), '.2f'))
        elif deal['finished?'] == False:
            this_profitpst = str(deal['actual_profit_percentage'])
            this_profitusd = str(format(float(deal['actual_usd_profit']), '.2f'))
        else:
            this_profit = "err"

        if me_want == "today":
            show_openclosed = True
            if str(date.today()) in str(deal['created_at']) or str(date.today()) in str(deal['closed_at']) or str(deal['closed_at']) == "None":
                if deal['bot_name'] != prev_botname:
                    if this_bot_sum != 0:
                        print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')), end = '')
                        print(" # Reserved: " + str(format(this_bot_reserved_sum, '.2f')), end = '')
                        print(" # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')), end = '')
                        print(" # OpenDeals: " + str(this_bot_opendeals), end = '')
                        print(" # ClosedDeals: " + str(this_bot_closeddeals))
                        grandtotal_bot_sum = grandtotal_bot_sum + this_bot_sum
                        grandtotal_bot_closed_sum = grandtotal_bot_closed_sum + this_bot_closed_sum
                        grandtotal_bot_reserved_sum = grandtotal_bot_reserved_sum + this_bot_reserved_sum
                    this_bot_opendeals    = 0
                    this_bot_closeddeals  = 0
                    this_bot_closed_sum   = 0
                    this_bot_reserved_sum = 0
                    this_bot_sum = float(this_profitusd)
                    if deal['finished?'] == True:
                        this_bot_closed_sum  = float(this_profitusd)
                        this_bot_closeddeals = 1
                    elif deal['finished?'] == False:
                        this_bot_reserved_sum = float(this_profitusd)
                        this_bot_opendeals    = 1

                    print("----------------------------------------------------------------")
                    print("BotName: " + str(deal['bot_name']), end = '')
                    try:
                        error, bot = p3cw.request( entity='bots', action='show', action_id=str(deal['bot_id']) )
                        print(" # ENABLED: " + str(bot['is_enabled']))
                    except:
                        print(" # ENABLED: DELETED")
                        
                    if argument2 != "totals":
                        print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-11s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")
                        
                else:
                    this_bot_sum = float(this_profitusd) + this_bot_sum
                    if deal['finished?'] == True:
                        this_bot_closed_sum  = float(this_profitusd) + this_bot_closed_sum
                        this_bot_closeddeals = int(this_bot_closeddeals) + 1
                    elif deal['finished?'] == False:
                        this_bot_reserved_sum = float(this_profitusd) + this_bot_reserved_sum
                        this_bot_opendeals    = int(this_bot_opendeals) + 1
                    
                    if argument2 != "totals":
                        print("Start: " + str(deal['created_at']), end = '')
                        print(" # Stop: " + '%-24s' % str(deal['closed_at']), end = '')
                        print(" # Pair: " + '%-11s' % str(deal['pair']), end = '')
                        print(" # Status: " + '%-11s' % str(deal['status']), end = '')
                        print(" # SO: " + str(deal['completed_safety_orders_count']), end = '')
                        print("(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']), end = '')
                        print(" # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD", end = '')
                        print("")

        if me_want == "active":
            if str(deal['closed_at']) == "None":
                if deal['bot_name'] != prev_botname:
                    if this_bot_sum != 0:
                        print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')) + " # Reserved: " + str(format(this_bot_reserved_sum, '.2f')) + " # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')))
                        grandtotal_bot_sum = grandtotal_bot_sum + this_bot_sum
                        grandtotal_bot_closed_sum = grandtotal_bot_closed_sum + this_bot_closed_sum
                        grandtotal_bot_reserved_sum = grandtotal_bot_reserved_sum + this_bot_reserved_sum
                    this_bot_closed_sum = 0
                    this_bot_reserved_sum = 0
                    this_bot_sum = float(this_profitusd)
                    if deal['finished?'] == True:
                        this_bot_closed_sum = float(this_profitusd)
                    elif deal['finished?'] == False:
                        this_bot_reserved_sum = float(this_profitusd)

                    print("----------------------------------------------------------------")
                    print("BotName: " + str(deal['bot_name']), end = '')
                    try:
                        error, bot = p3cw.request( entity='bots', action='show', action_id=str(deal['bot_id']) )
                        print(" # ENABLED: " + str(bot['is_enabled']))
                    except:
                        print(" # ENABLED: DELETED")
                        
                    print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-11s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")
                else:
                    this_bot_sum = float(this_profitusd) + this_bot_sum
                    if deal['finished?'] == True:
                        this_bot_closed_sum = float(this_profitusd) + this_bot_closed_sum
                    elif deal['finished?'] == False:
                        this_bot_reserved_sum = float(this_profitusd) + this_bot_reserved_sum
                    print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-11s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")


        elif me_want == "all":
            show_openclosed = True
            if deal['bot_name'] != prev_botname:
                if this_bot_sum != 0:
                    #print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')) + " # Reserved: " + str(format(this_bot_reserved_sum, '.2f')) + " # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')))
                    print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')), end = '')
                    print(" # Reserved: " + str(format(this_bot_reserved_sum, '.2f')), end = '')
                    print(" # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')), end = '')
                    print(" # OpenDeals: " + str(this_bot_opendeals), end = '')
                    print(" # ClosedDeals: " + str(this_bot_closeddeals))

                    grandtotal_bot_sum = grandtotal_bot_sum + this_bot_sum
                    grandtotal_bot_closed_sum = grandtotal_bot_closed_sum + this_bot_closed_sum
                    grandtotal_bot_reserved_sum = grandtotal_bot_reserved_sum + this_bot_reserved_sum
                this_bot_opendeals    = 0
                this_bot_closeddeals  = 0
                this_bot_closed_sum   = 0
                this_bot_reserved_sum = 0
                this_bot_sum = float(this_profitusd)
                if deal['finished?'] == True:
                    this_bot_closed_sum  = float(this_profitusd)
                    this_bot_closeddeals = 1
                elif deal['finished?'] == False:
                    this_bot_reserved_sum = float(this_profitusd)
                    this_bot_opendeals  = 1

                print("----------------------------------------------------------------")
                print("BotName: " + str(deal['bot_name']), end = '')
                try:
                    error, bot = p3cw.request( entity='bots', action='show', action_id=str(deal['bot_id']) )
                    print(" # ENABLED: " + str(bot['is_enabled']))
                except:
                    print(" # ENABLED: DELETED")

                print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-12s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")
            else:
                this_bot_sum = float(this_profitusd) + this_bot_sum
                if deal['finished?'] == True:
                    this_bot_closed_sum  = float(this_profitusd) + this_bot_closed_sum
                    this_bot_closeddeals = int(this_bot_closeddeals) + 1
                elif deal['finished?'] == False:
                    this_bot_reserved_sum = float(this_profitusd) + this_bot_reserved_sum
                    this_bot_opendeals  = int(this_bot_opendeals) + 1
                print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-12s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")


        else:
            if str(me_want) in str(deal['created_at']) or str(me_want) in str(deal['closed_at']):
                show_openclosed = True
                if deal['bot_name'] != prev_botname:
                    if this_bot_sum != 0:
                        #print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')) + " # Reserved: " + str(format(this_bot_reserved_sum, '.2f')) + " # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')))
                        print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')), end = '')
                        print(" # Reserved: " + str(format(this_bot_reserved_sum, '.2f')), end = '')
                        print(" # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')), end = '')
                        print(" # OpenDeals: " + str(this_bot_opendeals), end = '')
                        print(" # ClosedDeals: " + str(this_bot_closeddeals))
                        
                        grandtotal_bot_sum = grandtotal_bot_sum + this_bot_sum
                        grandtotal_bot_closed_sum = grandtotal_bot_closed_sum + this_bot_closed_sum
                        grandtotal_bot_reserved_sum = grandtotal_bot_reserved_sum + this_bot_reserved_sum
                    this_bot_opendeals    = 0
                    this_bot_closeddeals  = 0
                    this_bot_closed_sum = 0
                    this_bot_reserved_sum = 0
                    this_bot_sum = float(this_profitusd)
                    if deal['finished?'] == True:
                        this_bot_closed_sum  = float(this_profitusd)
                        this_bot_closeddeals = 1
                    elif deal['finished?'] == False:
                        this_bot_reserved_sum = float(this_profitusd)
                        this_bot_opendeals = 1

                    print("----------------------------------------------------------------")
                    print("BotName: " + str(deal['bot_name']), end = '')
                    try:
                        error, bot = p3cw.request( entity='bots', action='show', action_id=str(deal['bot_id']) )
                        print(" # ENABLED: " + str(bot['is_enabled']))
                    except:
                        print(" # ENABLED: DELETED")
                        
                    print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-12s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")
                else:
                    this_bot_sum = float(this_profitusd) + this_bot_sum
                    if deal['finished?'] == True:
                        this_bot_closed_sum  = float(this_profitusd) + this_bot_closed_sum
                        this_bot_closeddeals = int(this_bot_closeddeals) + 1
                    elif deal['finished?'] == False:
                        this_bot_reserved_sum = float(this_profitusd) + this_bot_reserved_sum
                        this_bot_opendeals  = int(this_bot_opendeals) + 1
                    print("Start: " + str(deal['created_at']) + " # Stop: " + '%-24s' % str(deal['closed_at']) + " # Pair: " + '%-12s' % str(deal['pair']) + " # Status: " + '%-11s' % str(deal['status']) + " # SO: " + str(deal['completed_safety_orders_count']) + "(+" + str(deal['completed_manual_safety_orders_count']) + ")/" + str(deal['max_safety_orders']) + " # Profit: " + '%6s' % str(this_profitpst) + "% / " + str(this_profitusd) + " USD")
            
        prev_botname = deal['bot_name']
    if this_bot_sum != 0:
        # print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')) + " # Reserved: " + str(format(this_bot_reserved_sum, '.2f')) + " # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')))
        print("BotCompletedSum: " + str(format(this_bot_closed_sum, '.2f')), end = '')
        print(" # Reserved: " + str(format(this_bot_reserved_sum, '.2f')), end = '')
        print(" # IfPanicSellAll: " + str(format(this_bot_sum, '.2f')), end = '')
        if show_openclosed == True:
            print(" # OpenDeals: " + str(this_bot_opendeals), end = '')
            print(" # ClosedDeals: " + str(this_bot_closeddeals), end = '')
        print("")

        grandtotal_bot_sum = grandtotal_bot_sum + this_bot_sum
        grandtotal_bot_closed_sum = grandtotal_bot_closed_sum + this_bot_closed_sum
        grandtotal_bot_reserved_sum = grandtotal_bot_reserved_sum + this_bot_reserved_sum

print()
print('##########################################################################################')
print("TotalCompleted : " + str(format(grandtotal_bot_closed_sum, '.2f')))
print("TotalReserved  : " + str(format(grandtotal_bot_reserved_sum, '.2f')))
print("TotalIfPanic   : " + str(format(grandtotal_bot_sum, '.2f')))
