#!/bin/bash

# MAKE SURE YOU FIRST SETUP KEYS
# USING THE COMMANDS:
# ssh-keygen -t rsa
# ssh-copy-id localuser@studvm38-p.cs.ucl.ac.uk

pg_dump -C postgres | bzip2 | ssh localuser@studvm38-p.cs.ucl.ac.uk "psql postgres -c 'DROP DATABASE postgres'; unzip2 | psql postgres"
