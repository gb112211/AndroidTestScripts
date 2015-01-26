#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2015年1月23日

@author: xuxu
'''
class SriptException(Exception):
    def __init__(self, str):
        self.str = str
    
    def _str_(self):
        return self.str
