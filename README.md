# 3commas-tools

## 3c-bot-stats
### Python3 script for getting an overview of your 3Commas deals
<p>I mostly use this to check the performance of different bots in my paper account. Which bots have earned the most today without gathering too many red bags?</p>
<p>To change between real account and paper account use your browser to go to the 3c dashboard and change there. It is a global setting and will affect the account this script use.</p>
<p>The script is a total hack and comes with no warranties. I recommend setting it up with a read only API key. Python is not my primary language either, but I start to like it :-)</p>

Screenshot:<br>
<img src="https://user-images.githubusercontent.com/2580262/120374281-a97be580-c319-11eb-934c-eab07f47e6c0.png" width=700>

## Installation
```
# Linux
# requires python3 to be installed
pip3 install py3cw
git clone https://github.com/gunleik/3c-bot-stats.git

# Windows
# click "Code" and download zip, extract it somewhere on you windows computer
# requires python3 to be installed https://www.python.org/downloads/
# and in the PATH
pip install py3cw 

# Windows binary
# I've made a Windows binary with Pyinstaller, so if you trust me
# and windows havent decided to block it as they often do with
# uncommon exe's, then you can try this one:
# https://github.com/gunleik/binaries/raw/main/3c-bot-stats.zip or
# https://github.com/gunleik/binaries/raw/main/3c-bot-stats_extract.exe
```

## Generate API key
If not done already, you have to create an API key at https://3commas.io/api_access_tokens.
It needs minimum "Account Read" and "Bots Read" access.
The first time you run the script it will ask for your API key and secret.
The script will save it in $HOME/.3c_keys (or 3c_keys.bat on Windows).
If you like to change the API key/secret or wipe it from you system, just delete the $HOME/.3c_keys file (or 3c_keys.bat).
	
## Run the scripts
```
# Use 3c_bot_stats.bat on windows
./3c_bot_stats.sh today        # filter on deals that have started or stopped today or is currently running
./3c_bot_stats.sh              # today is default and can be omitted
./3c_bot_stats.sh today totals # will not show each deal, just show the total stats of each bot
./3c_bot_stats.sh active       # show only active/running deals
./3c_bot_stats.sh all          # show all deals (limit on 1000)
./3c_bot_stats.sh 2021-05-31   # filter on a part of date/time, could be 2021-05 for year-month or 2021-05-31T14:55 to narrow down to specific time
```

## Nice to know
* In 3c-bot-stats: "Stop: None" means that this is an active deal.
* The use of paper account or real account is set globally on you account, so to use this scripts on paper account, go to 3commas web console and click paper account there. Then the script will automatically use the paper account and vice versa.

## Additional API info:
* https://github.com/3commas-io/3commas-official-api-docs
* https://github.com/bogdanteodoru/py3cw
