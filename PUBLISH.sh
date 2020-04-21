#!/bin/sh

HOST=$1

# On error, exit:
set -e

BASEDIR=$(pwd)/$(dirname "$BASH_SOURCE")
echo "$BASEDIR"

echo "DELETING BUILD PATH\n"
rm -rf "$BASEDIR/build/"
rm -rf "$BASEDIR/dist/"
rm -rf "$BASEDIR/*.egg-info"

echo "BUILDING\n"
python "$BASEDIR/setup.py" sdist

cd dist

echo "SENDING artifact .tar.gz to server instance.\n"
scp rio_gps*.tar.gz "${HOST}:~"

echo "FINISHED SUCCESSFULLY!"