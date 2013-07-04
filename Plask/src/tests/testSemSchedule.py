'''
Created on Jul 1, 2013

@author: moz
'''
import unittest
from Storage.Schedule import SemesterSchedule
import StringIO

SemA = "Sem_A"
SemACsvData = '''Course\tTeacher\tECTS\tWeeks\tLessons
Intro\tSUN\t0.5\t35\t6
Intro\tSUN\t0.5\t36\t8
Communication\tPETH\t2\t35-41,43\t4
'''
ClassA = "Class_A"
ScheduleSemAList = [{'Course': 'Intro', 'Teacher': 'SUN', 'ECTS': 0.5, 'Lessons': { 35: 6, 36: 8 }}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 
                     'Lessons': {35: 4, 36: 4,37: 4, 38: 4,39: 4, 40: 4, 41: 4, 43: 4}}, 
                    ]

class LocalDataMock:
    def getFile(self, filename ):
        return StringIO.StringIO( SemACsvData )

class Test(unittest.TestCase):


    def testSchedule(self):
        s = SemesterSchedule( LocalDataMock() )
        self.assertEqual( s.getList( SemA, ClassA ), ScheduleSemAList )
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSchedule']
    unittest.main()