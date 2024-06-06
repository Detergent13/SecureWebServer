sleep 30

# Check if another instance is already running
pid_file="/home/ec2-user/.check-request.pid"
if [ -f "$pid_file" ] && kill -0 $(cat "$pid_file") 2>/dev/null; then
    exit 0
fi
echo $$ > "$pid_file"

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
    echo "Running!"
    ./checker.py > latest.txt
    date >> latest.txt
fi
