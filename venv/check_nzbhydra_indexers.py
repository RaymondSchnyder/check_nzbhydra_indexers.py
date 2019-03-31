#!/usr/bin/env python3
import requests, pprint, json, re

try:
    with open("config.json") as config_file:
        try:
            config = json.load(config_file)
        except(json.decoder.JSONDecodeError):
            print("something in ya JSON is broken dude, validate the syntax!")
            exit(1)
except(FileNotFoundError):
    print("you forgot creating the config.json lol...")
    exit(1)
r = requests.get(config["uri"], auth=(config["username"], config["password"]))

try:
    for item in r.json():
        if item["state"] == "DISABLED_SYSTEM_TEMPORARY":
            if "apikey" in item["lastError"] :
                lastError = re.sub("[a-f0-9]{32}", "REDACTED", item["lastError"])
            else:
                lastError = item["lastError"]
            print("Indexer \"" + item["indexer"] + "\" is broken! Reason: " + lastError)
            exitstatus=1
    if exitstatus is 1:
        exit(1)
except(AttributeError):
    print("ERROR: JSON not found")
    exit(1)
except(json.decoder.JSONDecodeError):
    print("ERROR: JSON could not be decoded!")
    exit(1)
exit(0)