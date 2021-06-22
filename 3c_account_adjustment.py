
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
from pathlib import Path

home_dir             = str(Path.home())
inifile              = "3c_account_adjustment_default.ini"
my_action            = "testapply"
my_autoall           = ""
log_min              = False
bullish_level_auto   = ""
my_minimal           = ""

arguments   = len(sys.argv) - 1
if arguments > 0:
    for this_argument in sys.argv:
        if ".ini" in this_argument:
            inifile  = this_argument
        if this_argument == "apply" or this_argument == "testapply":
            my_action = this_argument
        if this_argument == "all":
            my_autoall = this_argument
        if this_argument == "minimal":
            my_minimal = "minimal"
        if my_autoall == 'all':
            try:
                tmp = int(this_argument)
                bullish_level_auto = this_argument
            except:
                tmp = 'do nothing'

        if this_argument == "--help":
            print()
            print("Usage: ./3c_account_adjustment.sh [my_settings.ini] [all NN] [apply|testapply]")
            print()
            print("Default settings found in 3c_account_adjustment_default.ini")
            print()
            print("optional arguments:")
            print("    apply,               apply rebalance with the settings generated")
            print("    testapply, (default) do a dryrun of the apply to check for error messages")
            print("    all NN,              skip asking for how bullish and set it automatically to integer number NN")
            print("    minimal,             show minimal output")
            print("    my_settings.ini,     alternative settings file")
            print()
            sys.exit()



config = configparser.ConfigParser()
config.read(inifile)

account_ids         = dict()
market_currency     = dict()
preferred_ratio     = dict()
allowed_deviation   = dict()

account_ids_raw = config['Accounts']['account_ids'].split(",")
for this_account_id in account_ids_raw:
    this_account_id_pair = this_account_id.strip().split(":")
    account_ids[this_account_id_pair[0]] = this_account_id_pair[1]

    market_currency[this_account_id_pair[0]] = dict()
    market_currency_raw = config['Accounts']['market_currency_' + this_account_id_pair[0]].split(",")
    for this_market_currency in market_currency_raw:
        market_currency[this_account_id_pair[0]] = this_market_currency.strip()

    preferred_ratio[this_account_id_pair[0]] = dict()
    preferred_ratio_raw = config['Accounts']['preferred_ratio_' + this_account_id_pair[0]].split(",")
    for this_preferred_ratio in preferred_ratio_raw:
        this_preferred_ratio_pair = this_preferred_ratio.strip().split(":")
        preferred_ratio[this_account_id_pair[0]][this_preferred_ratio_pair[0]] = this_preferred_ratio_pair[1]

    allowed_deviation[this_account_id_pair[0]] = dict()
    allowed_deviation_raw = config['Accounts']['allowed_deviation_' + this_account_id_pair[0]].split(",")
    for this_allowed_deviation in allowed_deviation_raw:
        allowed_deviation[this_account_id_pair[0]] = this_allowed_deviation.strip()

#pprint(account_ids)
#pprint(market_currency)
#pprint(preferred_ratio)
#pprint(allowed_deviation)


    


for account_id in account_ids:
    if account_id == 'Binance_main':
        if account_ids['Binance_main'] == '12345678':
            print("Please edit the 3c_account_adjustment_default.ini file or")
            print("specify an alternative ini-file as command line argument.")
            print("Use --help for list of arguments.")
            sys.exit()

    if bullish_level_auto != "":
        bullish_level = bullish_level_auto
    else:
        print()
        print("#########################################################################################################################")
        print("#########################################################################################################################")
        print("Account: " + str(account_id))
        print("How bullish are you today for account: " + str(account_id) + "?")
        print("    0   = polarbearish, keep all your funds in the market currency")
        print("    30  = bearish,     put 30% of your funds in crypto, around 70% kept in market currency")
        print("    70  = bullish,     put 70% of your funds in crypto, around 30% kept in market currency")
        print("    100 = bulls-on-paradeish, all-in on crypto (fund errors might occur because of rounding, better use 99)")
        print("    *   = enter or anything other than 0-100 will skip this account and keep current levels")
        bullish_level = input("So how bullish are you today for account: " + str(account_id) + "? (0-100): ")


    try:
        tmp = int(bullish_level)
        if float(bullish_level) >= 0 and float(bullish_level) <= 100:
            print()
            print(str(account_id), end=' # ')
            print(account_ids[account_id], end=' # ')
            print("market_cur=" + market_currency[account_id], end=' # ')
            print("pref_ratios=", end='')

            this_asset_preferred_ratio = ""
            this_total_ratio           = 0
            for this_asset in preferred_ratio[account_id]:
                this_set_ratio = (float(preferred_ratio[account_id][this_asset]) * float(bullish_level)) / 100
                this_asset_preferred_ratio = str(this_asset_preferred_ratio) + this_asset + ":" + str(this_set_ratio) + ", "
                this_total_ratio = this_total_ratio + float(this_set_ratio)

            market_currency_ratio      = 100 - float(this_total_ratio)
            this_asset_preferred_ratio = this_asset_preferred_ratio + market_currency[account_id] + ":" + str(market_currency_ratio)
            print(this_asset_preferred_ratio, end=' # ')
            print("allowed_dev=" + allowed_deviation[account_id], end=' # ')
            print("cfg=" + home_dir + '/3c_account_adjustedrebalancing_' + str(account_id) + '.ini')
            print()

            f = open(home_dir + "/3c_account_adjustedrebalancing_" + str(account_id) + ".ini", "w")
            f.write("[Account]\n")
            f.write("account_name        = " + str(account_id) + "\n")
            f.write("account_id          = " + account_ids[account_id] + "\n")
            f.write("market_currency     = " + market_currency[account_id] + "\n")
            f.write("preferred_ratio     = " + this_asset_preferred_ratio + "\n")
            f.write("allowed_deviation   = " + allowed_deviation[account_id] + "\n")
            f.close()

            if my_action == 'apply' or my_action == 'testapply':
                os.system('python3 3c_account_rebalancing.py ' + home_dir + '/3c_account_adjustedrebalancing_' + str(account_id) + '.ini ' + my_action + " " + my_minimal)
        else:
            print()
            print("###########################################")
            print("Skipping this account, value outside 0-100")
            print("###########################################")
    except:
        print()
        print("#############################################################")
        print("Skipping this account, non int given")
        print("If ini file exists I will give you the account overview here:")
        print("#############################################################")
        if Path(home_dir + '/3c_account_adjustedrebalancing_' + str(account_id) + '.ini').is_file():
            os.system('python3 3c_account_rebalancing.py ' + home_dir + '/3c_account_adjustedrebalancing_' + str(account_id) + '.ini')
