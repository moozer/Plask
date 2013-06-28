'''
Created on Jun 28, 2013

@author: moz
'''
import unittest
from Storage.LocalData import LocalData

DataDir = "../testData"
TestSemesters = ["Sem_A"]
TestCourses1 = ['Course_A', 'Course_B']
#TestCourses =

class Test(unittest.TestCase):


    def testLocalFiles(self):
        data = LocalData( DataDir )
        self.assertEqual( data.getCourses( TestSemesters[0] ), TestCourses1 )
        self.assertEqual( data.getSemesters(), TestSemesters )



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocalFiles']
    unittest.main()