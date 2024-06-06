#!/bin/bash

inotifywait -m /var/www /var/www/html /home/dexter/.ssh /home/skyler/.ssh /home/matty/.ssh /root/.ssh -e create -e moved_to -e modify -e delete |     while read dir action file; do   curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"'$action' done to '$file' in directory '$dir'\"}" "https://hooks.slack.com/services/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";     done
