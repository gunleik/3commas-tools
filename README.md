# 3commas-tools

### Python3 command line tool for 3commas
<p>3c_bot_stats: I mostly use this to check the performance of different bots in my paper account. Which bots have earned the most today without gathering too many red bags?</p>
<p>3c_use_account: change between paper and real account to use with 3c_bot_stats.</p>
<p>3c_close_all_paper_deals: cancel or sell all deals in the paper account to get a fresh start with 3c_bot_stats.</p>
<p>3c_account_rebalancing: rebalance any 3commas connected account.</p>
<p>3c_account_adjustment: how bullish are you today? Script to quickly adjust rebalancing. If set in ini-file that you want 60% BTC and 40% ETH and when running the script you say you are 50% bullish, the account(s) will be adjusted so that BTC get 30% (60% of 50%) and ETH get 20% (40% of 50%) of you account total value. The market currency will have 50% of you account value.</p>
<p>3c_account_stats: show list of your accounts and their USD value.</p>
<p>These scripts is a total hack and comes with no warranties. Python is not my primary language either, but I start to like it. If you have improvements please submit them :-)</p>

Screenshot:<br>
<img src="https://user-images.githubusercontent.com/2580262/121309352-5fd76000-c902-11eb-8683-d087b06cff45.png" width=700>

## Installation
```
# Linux
# requires python3 to be installed
# and require git if you like to clone (if not, just download the files)
pip3 install py3cw
git clone https://github.com/gunleik/3commas-tools.git

# Windows
# click "Code" and download zip, extract it somewhere on you windows computer
# requires python3 to be installed https://www.python.org/downloads/
# and in the PATH
pip install py3cw 
```

## Generate API key
If not done already, you have to create an API key at https://3commas.io/api_access_tokens.
To get full functionality the API key have to be set up with all the access levels.
The first time you run the script it will ask for your API key and secret.
The script will save it in $HOME/.3c_keys (or 3c_keys.bat on Windows).
If you like to change the API key/secret or wipe it from you system, just delete the $HOME/.3c_keys file (or 3c_keys.bat).

## Run the scripts
```
# All the commands support --help to show a quick list of arguments

# 3c_bot_stats:
# Use 3c_bot_stats.sh for Linux and 3c_bot_stats.bat on windows
./3c_bot_stats.sh today                    # Filter on deals that have started or stopped today or is currently running
./3c_bot_stats.sh                          # Today is default and can be omitted
./3c_bot_stats.sh today totals             # Will not show each deal, just show the total stats of each bot
./3c_bot_stats.sh active                   # Show only active/running deals
./3c_bot_stats.sh all                      # Show all deals (limit on 1000)
./3c_bot_stats.sh 2021-05-31               # Filter on a part of date/time, could be 2021-05 for year-month or 2021-05-31T14:55 to narrow down to specific time'

# 3c_use_account change between paper and real account for the 3c_bot_stats script to use:
# this setting is set globally on your account, so setting this to paper on the command line will also change it to the active account in your web browser the next time you go there
./3c_use_account.sh paper                  # Set to paper account
./3c_use_account.sh real                   # Set to real account

# 3c_account_rebalancing rebalance any 3commas connected account:
./3c_account_rebalancing.sh                # Rebalance a 3commas connected account with settings found in 3c_account_rebalancing_default.ini
./3c_account_rebalancing.sh apply          # Apply rebalance settings found in the ini-file
./3c_account_rebalancing.sh apply minimal  # Apply and use minimal output, good for cron job that logs output to file
./3c_account_rebalancing.sh testapply      # Do a dryrun of the apply to check for error messages
./3c_account_rebalancing.sh 3c_account_rebalancing_othersettings.ini  # alternative settings file, so the script can be run for different accounts

# 3c_account_adjustment adjust rebalance on any 3commas connected account:
./3c_account_adjustment.sh                # Rebalance a 3commas connected account with settings found in 3c_account_adjustment_default.ini
./3c_account_adjustment.sh apply          # Apply rebalance settings found in the ini-file
./3c_account_adjustment.sh testapply      # Do a dryrun of the apply to check for error messages (default)
./3c_account_adjustment.sh ~/3c_account_adjustment_othersettings.ini  # alternative settings file

# 3c_close_all_paper_deals close all paper deals:
./3c_close_all_paper_deals.sh cancel       # Cancel all paper deals (leave them in the current asset)
./3c_close_all_paper_deals.sh panic_sell   # "Close at market price" for all paper deals (sell back to the original asset)

# 3c_account_stats show accounts with their USD value:
./3c_account_stats.sh                      # Default view
./3c_account_stats.sh minimal              # Hide some of the output for piping to log-file
./3c_account_stats.sh hidefutures          # E.g. FTX will show futures accounts with sililar value as your spot accounts, so the total becomes wrong. If you don't use futures you can hide them with this argument.
```

## Auto Rebalancing
```
# If you like to automatically rebalance your account regularly you can 
# in Linux add the script to cron (crontab -e).
# */30 * * * * means every 30 minutes, check out 
# https://crontab-generator.org/ if you want to change the interval.
# Make sure the paths are correct for your system.

*/30 * * * * cd ~/git/3commas-tools; ./3c_account_rebalancing.sh ~/3c_account_rebalancing_ftx-main.ini apply minimal >>~/3c_account_rebalancing_ftx-main.log 2>>~/3c_account_rebalancing_ftx-main.log

# The above command in crontab will run rebalancing every 30 minutes, 
# with settings from ~/3c_account_rebalancing_ftx-main.ini and log 
# output and errors to ~/3c_account_rebalancing_ftx-main.log
```

## Nice to know
* In 3c-bot-stats: "Stop: None" means that this is an active deal.
* The use of paper account or real account is set globally on you account, so to use this scripts on paper account, go to 3commas web console and click paper account there. Then the script will automatically use the paper account and vice versa.
* 3c_account_adjustment will generate ini-files in your home directory with the name 3c_account_adjustedrebalancing_ACCOUNT.ini that is compatible with the 3c_account_rebalancing script.

## Changelog
* 2021-06-19: added 3c_account_adjustment script
* 2021-06-13: paper close script; confirm the deal is paper before closing
* 2021-06-13: rebalancing script; if asset is not already in your wallet the script will now do the initial buy of it
* 2021-06-13: readme; removed windows binary, this will not be updated... please install python and run from command line

## Additional API info:
* https://github.com/3commas-io/3commas-official-api-docs
* https://github.com/bogdanteodoru/py3cw
