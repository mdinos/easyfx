#!/usr/bin/env python

from os import popen
import psutil

"""
    Loads a single patch into PD from the patches folder, and starts running, killing off existing 
    pd processes as necessary.
"""
def load_patch(file_name: str):
    try:
        # Try and kill off any pure-data instances already running.
        processes = {p.pid: p.info for p in psutil.process_iter(['pid', 'name', 'username']) if p.info['name'] == 'pd'}
        for p in processes:
            print('Killing process {}'.format(p))
            popen('kill {}'.format(p))
    except Exception as e:
        print(e)
    try:
        print('Attempting to load {} with pure data.'.format(file_name))
        process = popen("./pure-data/bin/pd -send \"{}\" -open \"{}\" &".format("pd dsp 1", file_name))
    except Exception as e:
        print(e)
    

"""
    Pushes a generic message up to PD via pdsend
"""
def send_message(port, message):
    print('sending {} message to pd on port {}'.format(message, port))
    popen("echo '{}' | ./pure-data/bin/pdsend {} localhost udp".format(message, port))