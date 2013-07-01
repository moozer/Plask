'''
Created on Jul 1, 2013

@author: moz
'''
import unittest
from Storage.Schedule import SemesterSchedule
import StringIO

SemA = "Sem_A"
SemACsvData = '''Course\tTeacher\tECTS\tWeeks
Intro\tSUN\t0\t35
Communication\tPETH\t2\t35-41,43
'''
ScheduleSemAList = [{'Course': 'Intro', 'Teacher': 'SUN', 'ECTS': 0, 'Week': 35}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 35}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 36}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 37}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 38}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 39}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 40}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 41}, 
                    {'Course': 'Communication', 'Teacher': 'PETH', 'ECTS': 2, 'Week': 43}
                    ]

class LocalDataMock:
    def getFile(self, filename):
        return StringIO.StringIO( SemACsvData )

class Test(unittest.TestCase):


    def testSchedule(self):
        s = SemesterSchedule( LocalDataMock() )
        self.assertEqual( s.getList( SemA ), ScheduleSemAList )
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSchedule']
    unittest.main()