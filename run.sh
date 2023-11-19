#!/bin/bash

# $1 = json file (camere.json)
# $2 = language (it, en, fr, de, es)

# check if provided arguments are correct
if [ $# -lt 1 ]; then
    echo "Usage: $0 <json file> [<languages>]"
    exit 1
fi

sudo docker run -v ./output:/app/output -v ./input:/app/input hotelmenu $1 $2