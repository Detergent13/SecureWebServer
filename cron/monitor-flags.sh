#!/bin/bash

inotifywait -m /var/www/flag.txt /root/flag.txt -r -e access | \
while read dir action file; do
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"channel> flag.txt in directory '$dir' opened!!\"}" \
        "https://hooks.slack.com/services/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"
done

