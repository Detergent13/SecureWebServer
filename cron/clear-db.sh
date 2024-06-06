#!/bin/bash --

cd /var/db

sqlite3 -batch $1 <<"EOF"
.open orders.db
# .tables
# .schema orders
# SELECT * FROM orders;
DELETE FROM orders WHERE clientIP='54.193.63.45' AND transactionId='dc1af-0c91c';
EOF
