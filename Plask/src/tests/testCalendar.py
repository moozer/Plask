'''
Created on Jun 28, 2013

@author: moz
'''
import unittest
from Storage.Calendars import HandinsCalendar
import datetime
import StringIO

DataDir = "../testData"

Semesters = ['Sem_A']
Courses_A = ['Course_A', 'Course_B']
Sem_A = Semesters[0]
Course_A = Courses_A[0]
TestHandins_AA = [{'Date': datetime.datetime(2013, 8, 13, 0, 0), 'Handin': 'Exam question A1', 
                   'Datestring': '13/08-13', 'Comment': '[Optional]'}, 
                  {'Date': datetime.datetime(2013, 9, 5, 0, 0), 'Handin': 'Exam question A2', 
                   'Datestring': '05/09-13', 'Comment': '[Optional]'}]
TestHandins_semA = [ {'Date': datetime.datetime(2013, 8, 13, 0, 0), 'Handin': 'Course_A: Exam question A1', 
                      'Datestring': '13/08-13', 'Comment': '[Optional]'}, 
                     {'Date': datetime.datetime(2013, 9, 5, 0, 0), 'Handin': 'Course_A: Exam question A2', 
                      'Datestring': '05/09-13', 'Comment': '[Optional]'},
                    {'Date': datetime.datetime(2013, 8, 13, 0, 0), 'Handin': 'Course_B: Exam question A1', 
                      'Datestring': '13/08-13', 'Comment': '[Optional]'}, 
                     {'Date': datetime.datetime(2013, 9, 5, 0, 0), 'Handin': 'Course_B: Exam question A2', 
                      'Datestring': '05/09-13', 'Comment': '[Optional]'} ]

class LocalDataMockSemesterA:
    def getFile(self, filename):
        return StringIO.StringIO('''Date\tHand-in\tComment
130813\tExam question A1\t[Optional]
130905\tExam question A2\t[Optional]
''')
        
    def getSemesters( self ):
        return Semesters
    
    def getCourses(self, sem ):
        return Courses_A

class Test(unittest.TestCase):


    def testHandinsList(self):
        HC = HandinsCalendar( LocalDataMockSemesterA() )
        hclist = HC.getHandinList( Sem_A, Course_A )
        
        self.assertEqual( hclist, TestHandins_AA )

    def testSemesterHandinsList(self):
        HC = HandinsCalendar( LocalDataMockSemesterA() )
        hclist = HC.getHandinsListSemester( Sem_A )

        self.assertEqual( hclist, TestHandins_semA )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testHandinsIcs']
    unittest.main()