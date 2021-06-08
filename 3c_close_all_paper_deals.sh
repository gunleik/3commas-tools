#!/bin/bash

if [ -f "$HOME/.3c_keys" ]; then
	source $HOME/.3c_keys
	python3 3c_close_all_paper_deals.py $1 $2
else
	echo "If not done already, you have to create an API key at https://3commas.io/api_access_tokens"
	echo "It needs minimum \"AccountWrite\" and \"BotsWrite\" access"
	echo
    echo "No existing $HOME/.3c_keys file, fill inn the API info here:"

	echo -n "3commas API key: "
	read threecommasapirwkey

	echo -n "3commas API secret: "
	read threecommasapirwsecret

	touch $HOME/.3c_keys
	chmod 600 $HOME/.3c_keys

	echo "export threecommas_key=\"$threecommasapirwkey\"" >$HOME/.3c_keys
	echo "export threecommas_secret=\"$threecommasapirwsecret\"" >>$HOME/.3c_keys

	source $HOME/.3c_keys
	python3 3c_close_all_paper_deals.py $1 $2
fi
