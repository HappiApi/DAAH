#!/bin/bash

# MAKE SURE YOU FIRST SETUP KEYS
# USING THE COMMANDS:
# ssh-keygen -t rsa
# ssh-copy-id localuser@studvm31-p.cs.ucl.ac.uk

pg_dump -C postgres | bzip2 | ssh localuser@studvm31-p.cs.ucl.ac.uk "psql postgres -c 'DROP DATABASE postgres'; bunzip2 | psql postgres"
