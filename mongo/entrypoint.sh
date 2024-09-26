#!/bin/bash
set -e

echo "Starting entrypoint script..."

echo "Environment Variables:"
echo "MONGO_URI=$MONGO_URI"

# Wait for MongoDB to become available using pymongo
echo "Waiting for MongoDB..."
until python -c "
import sys
from pymongo import MongoClient
import os

try:
    client = MongoClient(os.environ['MONGO_URI'], serverSelectionTimeoutMS=2000)
    client.admin.command('ping')
except Exception as e:
    sys.exit(1)
" ; do
  echo "MongoDB is unavailable - sleeping"
  sleep 10
done
echo "MongoDB is up - executing commands"


## Start your main application
## Start your main application in the background
# ---------------------------------
# python main.py


## Start an interactive shell
# ---------------------------------
# bash

## Proceed to CMD instruction (do not run python main.py here)
# ---------------------------------
exec "$@"
