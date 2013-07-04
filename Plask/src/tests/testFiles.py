'''
Created on Jun 28, 2013

@author: moz
'''
import unittest
from Storage.LocalData import LocalData
import os.path

DataDir = "../testData"
TestSemesters = ["Sem_A"]

TestClasses = {'Sem_A': ["Class_A"] }
TestAllClasses = {'Sem_A': ['Class_A']}

TestCourses1 = { 'Sem_A': { 'Class_A': ['Course_A', 'Sample course', 'Course_B']}}
TestCoursesBySemA = TestCourses1
TestAllCourses = TestCourses1

TestLinks = ['About', 'Link_A', 'Link_B', 'index']

class Test(unittest.TestCase):


    def testGetSemesters(self):
        data = LocalData( DataDir  )
        self.assertEqual( data.getSemesters(), TestSemesters )
        
    def testGetClasses(self):
        data = LocalData( DataDir  )        
        self.assertEqual( data.getClasses( TestSemesters[0]), TestClasses, )
        self.assertEqual( data.getClasses(), TestAllClasses, )

    def testGetCourses(self):
        data = LocalData( DataDir  )
        self.assertEqual( data.getCourses( TestSemesters[0], TestClasses[TestSemesters[0]][0] ), TestCourses1 )
        self.assertEqual( data.getCourses( TestSemesters[0] ), TestCoursesBySemA )
        self.assertEqual( data.getCourses( ), TestAllCourses )

    def testGetLinks(self):
        data = LocalData( DataDir  )
        self.assertEqual( data.getLinks(), TestLinks )


    def testGetFile(self):
        data = LocalData( DataDir  )
        content = data.getFile( TestLinks[0]+'.md').read()
        content2 = open( os.path.join( DataDir, TestLinks[0]+'.md' )).read()

        self.assertEqual( content, content2 )
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocalFiles']
    unittest.main()