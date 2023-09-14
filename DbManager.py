# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 20:51:09 2023

@author: Akhmedov
"""

import os
import sys
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

dirname = os.path.dirname(__file__)
sys.path.append(dirname)

import settings

class DbManager:
    def __init__(self):
        print("DbManager init.")
                
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(settings.GOOGLE_BOT_JSON, scope)
        client = gspread.authorize(creds)
        
        self.document = client.open(settings.GOOGLE_DOC_NAME)
    
    def updateCell(self, cell, msg, worksheetName='Log'):
        retry = 0
        while retry < 3:
            try:
                self.document.worksheet(worksheetName).update(cell, msg)
                return True
            except ConnectionError:
                retry += 1
                print("updateCell failed.", cell, msg)
                print("Sleep 3 minutes for retry", retry)
                time.sleep(3*60)
            except gspread.exceptions.APIError as e:
                err = str(e)
                print(err)
                retry += 1
                print("updateCell failed.", cell, msg)
                print("Sleep 3 minutes for retry", retry)
                time.sleep(3*60)
        
        return False
    
    def getCell(self, cell, worksheetName):
        retry = 0
        while retry < 3:
            try:
                return self.document.worksheet(worksheetName).acell(cell).value
            except ConnectionError:
                retry += 1
                print("getCell failed.", cell)
                print("Sleep 3 minutes for retry", retry)
                time.sleep(3*60)
            except gspread.exceptions.APIError as e:
                err = str(e)
                print(err)
                retry += 1
                print("updateCell failed.", cell)
                print("Sleep 3 minutes for retry", retry)
                time.sleep(3*60)
                
        return ''
        

instance = DbManager()

