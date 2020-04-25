# linode-cli obj setacl --acl-public streetwise ch_data.csv --cluster eu-central-1
# wget https://streetwise.eu-central-1.linodeobjects.com/ch_data.csv


INPUT=ch_data.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read Image_Key Filename Canton Latitude Longitude Camera_Angle Sequence_Key Captured_At Panorama
do
	echo "Processing: $Filename"
	linode-cli obj setacl --acl-public streetwise "enhanced/$Filename" --cluster eu-central-1
done < $INPUT
IFS=$OLDIFS 
