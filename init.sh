#!/bin/bash

echo "Cloning pure-data repo and installing python packages..."
git clone git@github.com:pure-data/pure-data.git
cd pure-data
./autogen.sh
./configure
make
cd -
pip install -r requirements.txt