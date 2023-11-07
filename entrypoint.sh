#!/bin/bash
# Start MongoDB
mongod --fork --logpath /var/log/mongod.log

# Start your application
gunicorn --bind "0.0.0.0:5000" --timeout 600 -w 4 main:app
