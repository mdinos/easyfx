#!/usr/bin/env python

from easyfx.easyfx import EasyFX

if __name__ == '__main__':
    root = EasyFX()
    root.run()
    root.controller.clean_up(True)