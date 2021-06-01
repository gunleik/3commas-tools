# 3c-bot-stats
## Python3 script for getting an overview of your deals
Screenshot:<br>
<img src="https://user-images.githubusercontent.com/2580262/120322376-a1558300-c2e4-11eb-990c-92296902fc9d.png" width=700>

## Installation
```
pip3 install py3cw
git clone https://github.com/gunleik/3c-bot-stats.git
```

## Generate API key
If not done already, you have to create an API key at https://3commas.io/api_access_tokens.
It needs minimum "Account Read" and "Bots Read" access.
The first time you run the script it will ask for your API key and secret.
The script will save it in $HOME/.3c_keys.
If you like to change the API key/secret or wipe it from you system, just delete the $HOME/.3c_keys file.
	
## Run the script
```
# filter on deals that have started or stopped today or is currently running
# today is default and can be omitted
./3c_bot_stats.sh today
./3c_bot_stats.sh

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
* The use of paper account or real account is set globally on you account, so to use this script on paper account, go to 3commas web console and click paper account there. Then the script will automatically use the paper account and vice versa.

## Additional API info:
* https://github.com/3commas-io/3commas-official-api-docs
* https://github.com/bogdanteodoru/py3cw
