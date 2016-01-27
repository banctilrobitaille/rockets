'''
Created on 2016-01-27

@author: rockets
'''

class BadCRCException(Exception):

    def __init__(self, params):
        
        self.message = params
        