'''
Created on Jun 28, 2013

@author: moz
'''
import unittest
from Storage.LocalData import LocalData
import os.path

DataDir = "../testData"
TestSemesters = ["Sem_A"]
TestCourses1 = ['Course_A', 'Course_B']
TestLinks = ['About', 'Link_A', 'Link_B', 'index']
TestClasses = ["Class_A"]

class Test(unittest.TestCase):


    def testLocalFiles(self):
        data = LocalData( DataDir  )
        self.assertEqual( data.getCourses( TestSemesters[0], TestClasses[0] ), TestCourses1 )
        self.assertEqual( data.getClasses( TestSemesters[0]), TestClasses, )
        self.assertEqual( data.getSemesters(), TestSemesters, )
        self.assertEqual( data.getLinks(), TestLinks )

    def testGetFile(self):
        data = LocalData( DataDir  )
        content = data.getFile( TestLinks[0]+'.md').read()
        content2 = open( os.path.join( DataDir, TestLinks[0]+'.md' )).read()

        self.assertEqual( content, content2 )
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocalFiles']
    unittest.main()