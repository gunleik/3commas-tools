
#################################################################
#
#   3commas account rebalancing
#   rebalance any 3commas attached account
#
#   https://github.com/gunleik/3commas-tools
#
#   @gunleik
#
#################################################################

import os
import sys
import configparser

from py3cw.request import Py3CW
from datetime import datetime
from pprint import pprint

inifile  = "3c_account_rebalancing_default.ini"
argument  = ""
arguments = len(sys.argv) - 1
if arguments > 0:
    argument = sys.argv[1]
    if ".ini" in argument:
        inifile  = sys.argv[1]
        if arguments > 1:
            argument = sys.argv[2]


config = configparser.ConfigParser()
config.read(inifile)

account_id          = int(config['Account1']['account_id'])
market_currency     = str(config['Account1']['market_currency'])
allowed_deviation   = float(config['Account1']['allowed_deviation'])

if account_id == 12345678:
    print("Please edit the 3c_account_rebalancing_default.ini file or")
    print("specify an alternative ini-file as first command line argument")
    sys.exit()

preferred_ratio     = dict()
preferred_ratio_raw = config['Account1']['preferred_ratio'].split(",")
for this_preferred_ratio in preferred_ratio_raw:
    this_asset_referred_ratio = this_preferred_ratio.strip().split(":")
    preferred_ratio[this_asset_referred_ratio[0]] = this_asset_referred_ratio[1]




p3cw = Py3CW(
    key=os.environ.get('threecommas_key').rstrip(),
    secret=os.environ.get('threecommas_secret').rstrip(),
    request_options={
        'request_timeout': 10,
        'nr_of_retries': 1,
        'retry_status_codes': [502]
    }
)

# info about accounts
error, account = p3cw.request(
    entity='accounts',
    action='load_balances',
    action_id=str(account_id)
)

account_amount_in_usd   = format(float(account['usd_amount']), '.2f')
market_code             = account['market_code']

# load balances
error, balances = p3cw.request(
    entity='accounts',
    action='account_table_data',
    action_id=str(account_id)
)

total_asset_percentage  = 0
total_asset_to_rebalance_percentage = 0
total_target_percentage = 0
target_amount_in_usd    = 0
action_to_market        = dict()

print("#########################################################################################################################")
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
print("Account: " + str(account['name']))
print("Preferred Ratios: " + str(config['Account1']['preferred_ratio']) + "  (+/-" + str(allowed_deviation) + "%)")
print()

for balance in balances:
    asset_currency          = balance['currency_code']
    asset_amount_in_asset   = float(balance['position'])
    asset_amount_in_usd     = float(balance['usd_value'])
    asset_amount_percent    = format(balance['percentage'], '.2f')
    
    try:
        asset_target_percent    = preferred_ratio[asset_currency]
        if asset_currency in preferred_ratio:
            asset_target_percent_min= float(preferred_ratio[asset_currency]) - float(allowed_deviation)
            asset_target_percent_max= float(preferred_ratio[asset_currency]) + float(allowed_deviation)
            target_amount_in_usd    = (float(account_amount_in_usd) * float(asset_target_percent)) / 100
            dev_amount_in_usd       = float(target_amount_in_usd)
            action_to_market[asset_currency] = {'action': 'buy', 'amount': dev_amount_in_usd}
            
            if float(asset_amount_percent) < float(asset_target_percent_min):
                balance_action      = "buy"
                target_amount_in_usd= (float(account_amount_in_usd) * float(asset_target_percent)) / 100
                dev_amount_in_usd   = float(target_amount_in_usd) - float(asset_amount_in_usd)
            
            elif float(asset_amount_percent) > float(asset_target_percent_max):
                balance_action      = "sell"
                target_amount_in_usd= (float(account_amount_in_usd) * float(asset_target_percent)) / 100
                dev_amount_in_usd   = float(asset_amount_in_usd) - float(target_amount_in_usd)
    
            else:
                balance_action      = "none"
                action_amount_cur   = 0
                target_amount_in_usd= (float(account_amount_in_usd) * float(asset_target_percent)) / 100
                dev_amount_in_usd   = 0
    
            
            if asset_currency == market_currency:
                balance_action      = "m-" + balance_action
                #action_amount_cur   = 0
                #dev_amount_in_usd   = 0
                
            
            action_to_market[asset_currency] = {'action': balance_action, 'amount': dev_amount_in_usd}
            
            
            
            #print("Account: " + str(account['name']), end = ' # ')
            print('%-8s' % str(asset_currency + ":") + '%11s' % str(format(asset_amount_in_asset, '.4f')), end = ' ')
            print("# USD:" + '%10s' % str("$" + format(asset_amount_in_usd, '.2f')), end = ' ')
            print("# Ratio:" + '%6s' % str(asset_amount_percent), end = '% ')
            print("# pref:" + '%4s' % str(asset_target_percent_min) + "-" + '%-4s' % str(asset_target_percent_max) + " ($" + '%9s' % str(format(target_amount_in_usd, '.2f')) + ")", end = ' ')
            print("# Action: " + '%6s' % balance_action, end = ' ')
            print("# Amount: $" + str(format(dev_amount_in_usd, '.2f')))
            
            total_asset_percentage = float(total_asset_percentage) + float(asset_amount_percent)
            total_asset_to_rebalance_percentage = float(total_asset_to_rebalance_percentage) + float(asset_amount_percent)
            total_target_percentage = float(total_target_percentage) + float(asset_target_percent)
    except:
        asset_currency          = balance['currency_code']
        asset_amount_in_asset   = float(balance['position'])
        asset_amount_in_usd     = float(balance['usd_value'])
        asset_amount_percent    = format(balance['percentage'], '.2f')
        total_asset_percentage  = float(total_asset_percentage) + float(asset_amount_percent)
        #print("Account: " + str(account['name']), end = ' # ')
        print('%-8s' % str(asset_currency + ":") + '%11s' % str(format(asset_amount_in_asset, '.4f')), end = ' ')
        print("# USD:" + '%10s' % str("$" + format(asset_amount_in_usd, '.2f')), end = ' ')
        print("# Ratio:" + '%6s' % str(format(float(asset_amount_percent), '.2f')) + "%", end = ' ')
        print("# Action: n/a")


print("-------------------------------------------------------------------------------------------------------------------------")
#print("Account: " + str(account['name']), end = ' # ')
print('%-8s' % "---:       --------", end = ' ')
print("# USD:" + '%10s' % str("$" + format(float(account_amount_in_usd), '.2f')), end = ' ')
print("# Ratio:" + '%11s' % str(format(total_asset_to_rebalance_percentage, '.2f') + "/" + format(total_asset_percentage, '.2f')) + "%", end = ' ')
print("# pref:" + '%7s' % str(total_target_percentage) + "%")
print("=========================================================================================================================")
print()


if argument == "apply" or argument == "testapply":
    print("Applying rebalancing (" + argument + "):")
    print()
    
    for this_asset in action_to_market:
        this_action = action_to_market[this_asset]['action']
        this_amount = action_to_market[this_asset]['amount']
        if this_action == 'sell':
            pair    = market_currency + "_" + this_asset
            error, conversion_info = p3cw.request(
                entity='accounts',
                action='currency_rates',
                payload={
                    'market_code': market_code,
                    'pair': pair
                }    
            )
            precision = conversion_info['minLotSize'].find('1') - conversion_info['minLotSize'].find('.')
            sell_asset_amount_exacto = float(this_amount) / float(conversion_info['bid'])
            sell_asset_amount        = float(round(sell_asset_amount_exacto, precision))
            print("Sell: ", end = '')
            print(str(this_asset), end = ' ')
            print(sell_asset_amount, end = '')
            
            try:
                minimumTrade = conversion_info['minTotal']
            except:
                minimumTrade = 0
            
            if float(sell_asset_amount) >= float(conversion_info['minLotSize']) and float(this_amount) >= float(minimumTrade):
                if argument == "apply":
                    error, smart_trade_sell  = p3cw.request(
                        entity='smart_trades_v2', 
                        action='new',
                        payload={
                            "account_id": account_id,
                            "pair": pair,
                            "instant": True,
                            "position": {
                                "type": "sell",
                                "order_type": "market",
                                "units": {
                                    "value": sell_asset_amount
                                }
                            }
                        }
                    )
                    try:
                        print(" # EXCH_ERROR: " + error['msg'], end = '')
                    except:
                        print(" # OK", end = '')

            else:
                print(" # ERROR: LotSize: (" + str(sell_asset_amount_exacto) + " < " + str(conversion_info['minLotSize']) + ") or Trade: (" + str(this_amount) + " " + str(market_currency) + " < " + str(minimumTrade) + " " + str(market_currency) + ")", end = '')

            print()
    
    
    for this_asset in action_to_market:
        this_action = action_to_market[this_asset]['action']
        this_amount = action_to_market[this_asset]['amount']
        if this_action == 'buy':
            pair    = market_currency + "_" + this_asset
            error, conversion_info = p3cw.request(
                entity='accounts',
                action='currency_rates',
                payload={
                    'market_code': market_code,
                    'pair': pair
                }    
            )
            precision = conversion_info['minLotSize'].find('1') - conversion_info['minLotSize'].find('.')
            #buy_asset_amount = float(round((float(this_amount) / float(conversion_info['ask'])), precision))
            buy_asset_amount_exacto = float(this_amount) / float(conversion_info['ask'])
            buy_asset_amount        = float(round(buy_asset_amount_exacto, precision))
            print("Buy : ", end = '')
            print(str(this_asset), end = ' ')
            print(buy_asset_amount, end = '')
    
            try:
                minimumTrade = conversion_info['minTotal']
            except:
                minimumTrade = 0
                
            if float(buy_asset_amount) >= float(conversion_info['minLotSize']) and float(this_amount) >= float(minimumTrade):
                if argument == "apply":
                    error, smart_trade_buy  = p3cw.request(
                        entity='smart_trades_v2', 
                        action='new',
                        payload={
                            "account_id": account_id,
                            "pair": pair,
                            "instant": True,
                            "position": {
                                "type": "buy",
                                "order_type": "market",
                                "units": {
                                    "value": buy_asset_amount
                                }
                            }
                        }
                    )
                    try:
                        print(" # EXCH_ERROR: " + error['msg'], end = '')
                    except:
                        print(" # OK", end = '')

            else:
                print(" # ERROR: LotSize: (" + str(buy_asset_amount_exacto) + " < " + str(conversion_info['minLotSize']) + ") or Trade: (" + str(this_amount) + " " + str(market_currency) + " < " + str(minimumTrade) + " " + str(market_currency) + ")", end = '')

            print()


