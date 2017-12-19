#!/usr/bin/env python

from amplpy import AMPL

def main():

    # Intialize and choose solver
    ampl = AMPL()
    ampl.eval('option solver cplex;')
    
    # Load model
    ampl.read('model.mod')
    
    ampl.solve()

if __name__ == "__main__":
    main()


