#!/bin/bash

if [ -f "$HOME/.3c_keys" ]; then
	source $HOME/.3c_keys
	python3 3c_account_stats.py $1 $2
else
	echo "If not done already, you have to create an API key at https://3commas.io/api_access_tokens"
	echo "It needs minimum \"Account Read\" and \"Bots Read\" access"
	echo
    echo "No existing $HOME/.3c_keys file, fill inn the API info here:"

	echo -n "3commas API key: "
	read threecommasapikey

	echo -n "3commas API secret: "
	read threecommasapisecret

	touch $HOME/.3c_keys
	chmod 600 $HOME/.3c_keys

	echo "export threecommas_key=\"$threecommasapikey\"" >$HOME/.3c_keys
	echo "export threecommas_secret=\"$threecommasapisecret\"" >>$HOME/.3c_keys

	source $HOME/.3c_keys
	python3 3c_account_stats.py $1 $2
fi
