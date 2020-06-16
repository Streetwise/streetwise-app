#!/bin/sh

# Corrects the ACLs and downloads latest image database

# Campaign 1
linode-cli obj setacl --acl-public streetwise campaigns/safety/ch-data-safety.csv --cluster eu-central-1
wget http://streetwise.eu-central-1.linodeobjects.com/campaigns/safety/ch-data-safety.csv

# Campaign 2
linode-cli obj setacl --acl-public streetwise campaigns/atmos/ch-data-atmos.csv --cluster eu-central-1
wget http://streetwise.eu-central-1.linodeobjects.com/campaigns/atmos/ch-data-atmos.csv
