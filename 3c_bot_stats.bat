@echo off

if exist 3c_keys.bat (
	3c_keys.bat
	python 3c_bot_stats.py %1
) else (
	echo If not done already, you have to create an API key at https://3commas.io/api_access_tokens
	echo It needs minimum "Account Read" and "Bots Read" access
	echo.
    echo No existing 3c_keys.bat file, fill inn the API info here:

	set /p threecommasapikey=3commas API key: 

	set /p threecommasapisecret=3commas API secret: 

	echo set threecommas_key=%threecommasapikey% >3c_keys.bat
	echo set threecommas_secret=%threecommasapisecret% >>3c_keys.bat

	3c_keys.bat
	python 3c_bot_stats.py %1
)
