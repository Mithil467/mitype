#!/usr/bin/env python

""" Called when command python -m mitype is executed """

from mitype.app import App

if __name__ == "__main__":
    OBJ = App()
    OBJ.start()
