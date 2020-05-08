#!/bin/sh

# Corrects the ACLs and downloads latest image database

linode-cli obj setacl --acl-public streetwise ch_data.csv --cluster eu-central-1
wget https://streetwise.eu-central-1.linodeobjects.com/ch_data.csv
