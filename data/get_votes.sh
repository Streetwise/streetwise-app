#!/bin/sh

url=$1
apikey=$2
timestamp=$(date "+%Y.%m.%d-%H.%M")
filename=streetwise-votes-$timestamp.json

echo Downloading votes from $url ...
curl -X GET "$url/api/vote/export" -H "accept: application/json" -H "authorization: $apikey" > $filename

echo $filename
