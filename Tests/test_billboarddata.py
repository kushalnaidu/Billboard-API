# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 20:05:24 2018

@author: kusha
"""

"""
Test for BillboardData:
"""
import billboard
from datetime import datetime
class TestBillboardData:
    def __init__(self):
        self.data = billboard.BillboardData()
    //test for all input variables
    def test_date(self):
        self.data.date