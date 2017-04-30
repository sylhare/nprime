# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:23:52 2017

@author: sylhare

"""
from __future__ import print_function #To make the end='' works in the print()
import pyprime as p
import unit_test as ut
import toolbox as tb

#Demo of Grphical Prime functions
p.sacksPlot()
p.ulamPlot()

#Demo of the Primarity testing functions
print(p.isPrime(7))
print(p.fermat(7))
print(p.millerRabin(7))

#Demo of the Prime generating functions
print(p.genPrimes(7))
print(p.findPrimes(2, 7, p.fermat))

#Demo of the unit_test functions
print(ut.unit_test(p.isPrime))

filepath = tb.save(ut.unit_test(p.isPrime), "test")
for x in tb.read(filepath):
    print(x, end='') #So there's no '\n' after each print