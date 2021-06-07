@echo off

if exist 3c_rw_keys.bat (
	3c_rw_keys.bat
	python 3c_account_rebalancing.py %1 %2
	pause
) else (
	echo If not done already, you have to create an API key at https://3commas.io/api_access_tokens
	echo It needs minimum "Account Read", "SmartTradesRead" and "SmartTradesWrite" access
	echo.
    echo No existing 3c_rw_keys.bat file, fill inn the API info here:

	set /p threecommasapirwkey=3commas API key: 
	set /p threecommasapirwsecret=3commas API secret: 
)

if not exist 3c_rw_keys.bat (
	echo set threecommas_rw_key=%threecommasapirwkey% >3c_rw_keys.bat
	echo set threecommas_rw_secret=%threecommasapirwsecret% >>3c_rw_keys.bat

	3c_rw_keys.bat
	python 3c_account_rebalancing.py %1 %2
	pause
)

