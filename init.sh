#!/bin/bash

echo "Cloning pure-data repo and installing python packages..."
git clone git@github.com:pure-data/pure-data.git
pip install -r requirements.txt