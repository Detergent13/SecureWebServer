#!/bin/bash --

cd /var/db

sqlite3 -batch $1 <<"EOF"
.open orders.db
.shell echo "\n-------- TABLES: --------\n"
.tables
.shell echo "\n-------- ORDERS SCHEMA: --------\n"
.schema orders
.shell echo "\n-------- ORDERS DB: --------\n"
SELECT * FROM orders;
EOF
