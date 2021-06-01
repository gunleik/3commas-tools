# 3c-bot-stats

## Python3 script for getting an overview of your 3Commas deals
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
```

## Generate API key
If not done already, you have to create an API key at https://3commas.io/api_access_tokens.
It needs minimum "Account Read" and "Bots Read" access.
The first time you run the script it will ask for your API key and secret.
The script will save it in $HOME/.3c_keys (or 3c_keys.bat on Windows).
If you like to change the API key/secret or wipe it from you system, just delete the $HOME/.3c_keys file.
	
## Run the script
```
# filter on deals that have started or stopped today or is currently running
# today is default and can be omitted
./3c_bot_stats.sh today
./3c_bot_stats.sh
# use 3c_bot_stats.bat on windows

# show all deals (limit on 1000)
./3c_bot_stats.sh all

# show deals that where started or stopped at given datetime filter
# eg. on filters can be:
# 2021
# 2021-05
# 2021-05-31
# 2021-05-31T14:55
./3c_bot_stats.sh 2021-05-31
```

## Nice to know
* Stop = None means that this is an active deal.
* The use of paper account or real account is set globally on you account, so to use this script on paper account, go to 3commas web console and click paper account there. Then the script will automatically use the paper account and vice versa.

## Additional API info:
* https://github.com/3commas-io/3commas-official-api-docs
* https://github.com/bogdanteodoru/py3cw
