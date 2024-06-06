#!/bin/bash

echo $(date)

BACKUP_PATH="/home/dexter/backup"
DATE=$(date +"%m-%d-%y")
HOUR=$(date +"%H")

if [ $HOUR == "11" ]
then
	NUM="1"
else
	NUM="2"
fi

FULL_PATH=$BACKUP_PATH"::"$DATE\_$NUM

echo $FULL_PATH

borg create --exclude /var/log --exclude /var/cache --exclude /var/backups --stats $FULL_PATH /home /etc /bin /srv /var /root
