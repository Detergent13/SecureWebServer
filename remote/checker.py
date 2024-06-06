#!/usr/bin/env python3

import sys
import requests
import re
import json

WEBHOOK_URL = "https://hooks.slack.com/services/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"


def main(firstName="John", lastName="Doe", phoneNumber="123", item="Owl"):
    URL = "https://team7.csc429.io/submit.php"
    transactionIdPattern = re.compile(r'([a-z]|\d){5}-([a-z]|\d){5}')
    data = {
        "firstName": firstName,
        "lastName": lastName,
        "phoneNumber": phoneNumber,
        "item": item
    }

    # Checks for successful POST request for submitting orders
    try:
        request = requests.post(url=URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=10)
        print(request.text)
        if request.status_code != 200:
            notify(f"Submit request gave wrong status response: {request.status_code}")
        return transactionIdPattern.search(request.text).group()
    except requests.exceptions.Timeout:
        notify(f"Submit request timed out!")
    except requests.exceptions.RequestException as e:
        notify(f"Submit request failed: {e}")


def notify(message):
    with open(".status", "r+") as file:
        if file.read() == 'down':
            print('We already know it\'s down, not re-triggering.')
            exit(0)
        else:
            print('New downtime, notifying!!')
            file.seek(0)
            file.write('down')
            file.truncate()

    url = 'https://events.pagerduty.com/v2/enqueue'
    headers = {'Content-Type': 'application/json'}
    data = {
        "payload": {
            "summary": message,
            "severity": "critical",
            "source": "Python checker"
        },
        "routing_key": "5524d5b5bb8c4902d0f8108c5c2a33ef",
        "event_action": "trigger"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)

    data = {"text": "<!channel>" + message}
    headers = {"Content-type": "application/json"}

    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)
    print(response.text)
    exit(1)


if __name__ == "__main__":
    expected = "dc1af-64570"
    if len(sys.argv) == 1:  # Use default values
        tid = main()
        if tid != expected:
            notify(f"Test transaction ID is not {expected}: {tid}")
        else:
            with open(".status", "r+") as file:
                    if file.read() != 'up':
                        file.seek(0)
                        file.write('up')
                        file.truncate()
                        data = {"text": "We\'re back up! Shoutout to whoever\'s on-call :^)"}
                        headers = {"Content-type": "application/json"}
                        response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)


            
    #elif len(sys.argv) == 5:
    #    main(*sys.argv[1:])
    else:
        print("Usage: python requests_checker.py [firstName lastName phoneNumber item]")
