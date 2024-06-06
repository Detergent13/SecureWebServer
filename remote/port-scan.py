#!/usr/bin/env python3

import nmap
import json
import socket
import requests
from datetime import datetime

WEBHOOK_URL = "https://hooks.slack.com/services/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"
NUM_SITES = 9
OUR_SITE = 7

print("START: ", datetime.now(), "\n")

# Define the host and ports to scan
hosts = [] # Replace with the desired host or IP address
for i in range(NUM_SITES):
    hosts.append(f"team{i+1}.csc429.io")

ips = []
print(socket.gethostbyname(hosts[0]))
for host in hosts:
    ips.append(socket.gethostbyname(host))
ports = "1-65535"  # Scan all ports

# Create an nmap scanner object
nm = nmap.PortScanner()
dlist = [""] * NUM_SITES
print(dlist)

for i in range(len(ips)):
    ip = ips[i]
    nm.scan(hosts=ip, arguments=f"-sV -O -p{ports}")

    open_ports = [port for port in nm[ip]['tcp'].keys() if nm[ip]['tcp'][port]['state'] == 'open'] 


    print(f"Open ports on {hosts[i]}:")
    for port in open_ports:
        print(f"Port {port}")

    with open(f"port_history/{i+1}.txt", "r") as file:
        old_ports = json.load(file)
        diff = set(open_ports) - set(old_ports)
        print(i)
        dlist[i] = diff

    # Store the open ports in a JSON file
    with open(f"port_history/{i+1}.txt", "w") as file:
        json.dump(open_ports, file)
output = "New ports!\n"
for i in range(len(dlist)):
   if dlist[i]:
        if i == OUR_SITE-1: # -1 for indexing
            output += "<!channel> IMPORTANT!:\n"
            
            url = 'https://events.pagerduty.com/v2/enqueue'
            headers = {'Content-Type': 'application/json'}
            data = {
                "payload": {
                    "summary": "Unknown port opened (check Slack)",
                    "severity": "critical",
                    "source": "port-scan.py"
                },
                "routing_key": "5524d5b5bb8c4902d0f8108c5c2a33ef",
                "event_action": "trigger"
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(response.text)
            
        output += f"{hosts[i]}:\n"
        output += str(dlist[i]) + "\n" 

if output != "New ports!\n":
    print(output)
    data = {"text": output}
    headers = {"Content-type": "application/json"}

    response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers=headers)
    print(response.text)

print("END: ", datetime.now(), "\n")
