#################################################################
#
#   3commas bot stats
#   giving a better overview of your deals in 3commas
#
#   https://github.com/gunleik/3commas-tools
#
#   @gunleik
#
#################################################################



import time
import sys
import os

from py3cw.request import Py3CW
from datetime import date
from pprint import pprint



my_action = ""
arguments = len(sys.argv) - 1
if arguments > 0:
    my_action = sys.argv[1]


if my_action == "--help":
    print()
    print("Usage: ./3c_use_account.sh [real|paper]")
    print()
    print("Use this to change active account to be used with 3c_bot_stats")
    print()
    print("arguments:")
    print("    real,        set active account to real account")
    print("    paper,       set active account to paper account")
    print()
    sys.exit()


if str(my_action) == "real" or str(my_action) == "paper":
    my_nothing = "yeay"
else:
    print("Expected argument: real / paper")
    print("Specify if I should change to real or paper account")
    sys.exit()
    


# initiate API with key/secret from os env
p3cw = Py3CW(
    key=os.environ.get('threecommas_key').rstrip(),
    secret=os.environ.get('threecommas_secret').rstrip(),
    request_options={
        'request_timeout': 10,
        'nr_of_retries': 1,
        'retry_status_codes': [502]
    }
)

# change to paper account requires api with account write access
# real or paper account is set on global account settings, so manually changing
# this in the 3c web console makes the setting for this script also
error, mode = p3cw.request(
    entity='users',
    action='change_mode',
    payload={
        "mode": str(my_action)
    }
)
if mode == True:
	print("Changed to use account: " + str(my_action))
else:
	print("Something failed:")
	pprint(error)
