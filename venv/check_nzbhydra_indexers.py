#!/usr/bin/env python3
import requests, json, re, sys, getopt
from pprint import pprint
uri = ""
username = ""
password = ""
apikey = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:u:p:a:", ["site=", "username=", "password=", "apikey="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    sys.exit(1)

for o, a in opts:
    if o in ["-s", '--site']:
        uri = a
    elif o in ("-u", "--username"):
        username = a
    elif o in ("-p", "--password"):
        password = a
    elif o in ("-a", "--apikey"):
        apikey = a
    else:
            assert False, "unhandled option"

if uri is "":
    print("you forgot to provide the site uri with --site")
    exit(1)
elif username is "":
    print("you forgot to provide the username with --username")
    exit(1)
elif password is "":
    print("you forgot to provide the password with --password")
elif apikey is "":
    print("you forgot to provide the apikey with --apikey")
    exit(1)

payload = {
     'apikey': apikey
}

try:
    r = requests.get(uri, auth=(username, password), params=payload)
except(requests.exceptions.MissingSchema):
    print("Your URL is missing http:// or https://")
    exit(1)
exitstatus=0
try:
    for item in r.json():
        try:
            if item["state"] == "DISABLED_SYSTEM_TEMPORARY":
                if "apikey" in item["lastError"] :
                    lastError = re.sub("[a-f0-9]{32}", "REDACTED", item["lastError"])
                else:
                    lastError = item["lastError"]
                print("Indexer \"" + item["indexer"] + "\" is broken! Reason: " + lastError)
                exitstatus=1
        except TypeError:
            print("Returned JSON was faulty, error unknown")
            exitstatus=1
    if exitstatus is 1:
        exit(1)
except(AttributeError):
    print("ERROR: JSON not found")
    exit(1)
except(json.decoder.JSONDecodeError):
    print("ERROR: JSON could not be decoded!")
    exit(1)

print("everything seems alright :)")
exit(0)
