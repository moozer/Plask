'''
Created on Jun 28, 2013

@author: moz
'''
import unittest
from Storage.Calendars import HandinsCalendar
import datetime

DataDir = "../testData"

Sem_A = "Sem_A"
Course_A = "Course_A"
TestHandins_AA = [{'Date': datetime.datetime(2013, 8, 13, 0, 0), 'Handin': 'Exam question 1', 
                   'Datestring': '13/08-13', 'Comment': '[Optional]'}, 
                  {'Date': datetime.datetime(2013, 9, 5, 0, 0), 'Handin': 'Exam question 2', 
                   'Datestring': '05/09-13', 'Comment': '[Optional]'}]


class Test(unittest.TestCase):


    def testHandinsList(self):
        HC = HandinsCalendar(DataDir)
        hclist = HC.getHandinList( Sem_A, Course_A )
        
        self.assertEqual( hclist, TestHandins_AA )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testHandinsIcs']
    unittest.main()