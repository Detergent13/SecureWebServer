#!/bin/bash

# Check if another instance is already running
pid_file="/root/.check-apache-up.pid"
if [ -f "$pid_file" ] && kill -0 $(cat "$pid_file") 2>/dev/null; then
    exit 0
fi
echo $$ > "$pid_file"

WEBHOOK_URL="https://hooks.slack.com/services/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"

# Get current day and time
CURRENT_DAY=$(date +%A)
CURRENT_TIME=$(date +%H)

GRACE_START="08"
GRACE_END="11"

# Check if it's not Tuesday or Thursday and not between 8am and 11am
if [ "$CURRENT_TIME" -ge $GRACE_START ] && [ "$CURRENT_TIME" -lt $GRACE_END ] \
	&& ([ "$CURRENT_DAY" == "Tuesday" ] || [ "$CURRENT_DAY" == "Thursday" ]); then

    echo "It's Tuesday/Thursday 8am-11am. No message will be sent."
else
    # Check if Apache2 is running
    if systemctl is-active --quiet apache2.service; then
        echo "Apache2 is running."
    else
        echo "Apache2 is not running. Sending message to Slack..."

        # Message to send to Slack
	MESSAGE1="Apache is down! Trying an auto restart."
	MESSAGE2="Restart successful. No worries :)"
	MESSAGE3="<!channel> APACHE IS DOWN.\nPagerDuty has been triggered"
	MESSAGE4="Apache is back up! Shoutout to whoever's on-call :^)"

	curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$MESSAGE1\"}" $WEBHOOK_URL

	# Try a restart, exit if successful
	systemctl start apache2

	sleep 20

	if systemctl is-active --quiet apache2.service; then
		curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$MESSAGE2\"}" $WEBHOOK_URL
        	exit 0
	fi

	curl --request 'POST' --url 'https://events.pagerduty.com/v2/enqueue' --header 'Content-Type: application/json' \
		--data '{
	     		 "payload": {
	     		 "summary": "Apache2 not running",
	      		 "severity": "critical",
	     		 "source": "Server cronjob"
	 	 },
	  "routing_key": "5524d5b5bb8c4902d0f8108c5c2a33ef",
	  "event_action": "trigger"
	}'

        # Send message to Slack webhook
        curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$MESSAGE3\"}" $WEBHOOK_URL

        echo "Message sent to Slack. Waiting until it's fixed to finish execution."

	while ! systemctl is-active --quiet apache2.service; 
	do
		sleep 50
	done

	curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$MESSAGE4\"}" $WEBHOOK_URL
    fi
fi
