#!/bin/sh
rm test.db
sqlite3 test.db < tables.sql
python test.py
