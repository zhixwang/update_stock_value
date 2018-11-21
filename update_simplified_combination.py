# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 14:14:18 2018

@author: zxwan
"""

from invest_combination_simplified import auto_combination as acb
import argparse

# If define the exchange currency rate of HKD here in the command, no need to read from file then
ap = argparse.ArgumentParser(description='Update values')
ap.add_argument("-c", "--currency", required=False,type = float,
	help="Currency")
args = vars(ap.parse_args())

if args['currency']:
	curr = args['currency']
else:
	curr = 0
	
cb2 = acb(curr)
cb2.save()



