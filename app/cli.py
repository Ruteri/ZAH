#!/usr/bin/env python

import sys
from model.model import Model

def main():
    if len(sys.argv) < 2:
        print('Usage: {0} <data_dir>'.format(sys.argv[0]))
        return 1

    dataDirectory = sys.argv[1]
    model = Model(dataDirectory)
    carsUsage = model.run()
    print(carsUsage)

if __name__ == "__main__":
    main()
