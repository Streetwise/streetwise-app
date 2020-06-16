#!/bin/sh

[ ! $1 ] && { echo "<url> <apikey>"; exit 99; }

url=$1
apikey=$2
timestamp=$(date "+%Y.%m.%d-%H.%M")
filename=streetwise-votes-$timestamp.json

echo Downloading votes from $url ...
curl -X GET "$url/api/results/all" -H "accept: application/json" -H "authorization: $apikey" > $filename

echo $filename
