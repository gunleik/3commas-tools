# 3c-bot-stats
# Python3 script for getting an overview of the bots

You probably have to run this first:
```
pip3 install py3cw
```

Then run the script as follows:
```
# filter on deals that have started, stopped today or is currently running
# today is default and can be omitted
python3 3c_bot_stats.py today

# show all deals (limit on 1000)
python3 3c_bot_stats.py all

# show deals that where started or stopped at given datetime filter
# eg. on filters can be:
# 2021
# 2021-05
# 2021-05-31
# 2021-05-31T14:55
python3 3c_bot_stats.py 2021-05-31
```
