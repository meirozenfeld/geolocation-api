#!/bin/sh
mongo --bind_ip 0.0.0.0 &
python /var/www/server.py
