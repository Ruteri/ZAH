#!/usr/bin/env python

import sys
from model.model import Model

def rejected():
    print "rejected"

def notified():
    print "notified"

def done():
    print "done"

def main():
    if len(sys.argv) < 2:
        print('Usage: {0} <data_dir>'.format(sys.argv[0]))
        return 1

    dataDirectory = sys.argv[1]
    model = Model(dataDirectory)
    model.run(done, notified, rejected)

if __name__ == "__main__":
    main()
