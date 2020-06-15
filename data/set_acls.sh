#!/bin/sh

echo Trying to set ACLs with s3cmd ..
s3cmd setacl s3://streetwise.eu-central-1.linodeobjects.com/campaigns/ --acl-public --recursive

read -p "Did that work? Ctrl-C if it did."

echo Setting ACLs using linode-cli ..
INPUT=ch-data-atmos.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read Image_Key Filename Canton Latitude Longitude Camera_Angle Sequence_Key Captured_At Panorama Campaign Skip
do
	echo "Processing: $Filename"
	linode-cli obj setacl --acl-public streetwise "campaigns/$Campaign/images/$Filename" --cluster eu-central-1
done < $INPUT
IFS=$OLDIFS
