# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:23:52 2017

@author: sylhare

"""

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

tb.save(ut.unit_test(p.isPrime), "test")
for x in tb.read("../src/test_2017-03-28.txt"):
    print (x, end='')
