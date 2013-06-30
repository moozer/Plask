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
Course_A_csv = '''Date\tHand-in\tComment
130813\tExam question A1\t[Optional]
130905\tExam question A2\t[Optional]
'''
Course_A_ics = '''BEGIN:VCALENDAR\r
VERSION:2.0\r
PRODID:-//My calendar product//mxm.dk//\r
BEGIN:VEVENT\r
SUMMARY:Exam question A1\r
DTSTART;VALUE=DATE:20130813\r
DESCRIPTION:[Optional]\r
END:VEVENT\r
BEGIN:VEVENT\r
SUMMARY:Exam question A2\r
DTSTART;VALUE=DATE:20130905\r
DESCRIPTION:[Optional]\r
END:VEVENT\r
END:VCALENDAR\r
'''

Semester_A_ics = 'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//My calendar product//mxm.dk//\r\nBEGIN:VEVENT\r\nSUMMARY:Course_A: Exam question A1\r\nDTSTART;VALUE=DATE:20130813\r\nDESCRIPTION:[Optional]\r\nEND:VEVENT\r\nBEGIN:VEVENT\r\nSUMMARY:Course_A: Exam question A2\r\nDTSTART;VALUE=DATE:20130905\r\nDESCRIPTION:[Optional]\r\nEND:VEVENT\r\nBEGIN:VEVENT\r\nSUMMARY:Course_B: Exam question A1\r\nDTSTART;VALUE=DATE:20130813\r\nDESCRIPTION:[Optional]\r\nEND:VEVENT\r\nBEGIN:VEVENT\r\nSUMMARY:Course_B: Exam question A2\r\nDTSTART;VALUE=DATE:20130905\r\nDESCRIPTION:[Optional]\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n'

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
        return StringIO.StringIO( Course_A_csv )
        
    def getSemesters( self ):
        return Semesters
    
    def getCourses(self, sem ):
        return Courses_A

class LocalDataMockCourseAIcs:
    def getFile(self, filename):
        return StringIO.StringIO(Course_A_csv)

class LocalDataMockSemAIcs:
    def getSemesters( self ):
        return Semesters
    
    def getCourses(self, sem ):
        return Courses_A
    
    def getFile(self, filename):
        return StringIO.StringIO( Course_A_csv )
    
class Test(unittest.TestCase):


    def testHandinsList(self):
        HC = HandinsCalendar( LocalDataMockSemesterA() )
        hclist = HC.getHandinList( Sem_A, Course_A )
        
        self.assertEqual( hclist, TestHandins_AA )

    def testSemesterHandinsList(self):
        HC = HandinsCalendar( LocalDataMockSemesterA() )
        hclist = HC.getHandinsListSemester( Sem_A )

        self.assertEqual( hclist, TestHandins_semA )

    def testCourseIcs(self):
        HC = HandinsCalendar( LocalDataMockCourseAIcs() )
        hcics = HC.getCourseIcs( Sem_A, Course_A )

        self.assertEqual( hcics, Course_A_ics )
        
    def testSemesterIcs(self):
        HC = HandinsCalendar( LocalDataMockSemAIcs() )
        hcics = HC.getSemesterIcs( Sem_A  )

        self.assertEqual( hcics, Semester_A_ics )
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testHandinsIcs']
    unittest.main()
    
