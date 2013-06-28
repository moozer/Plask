'''
Created on Jun 28, 2013

@author: moz
'''
import unittest
from Storage.LocalData import LocalData

DataDir = "../testData"
TestSemesters = ["Sem_A"]
TestCourses1 = ['Course_A', 'Course_B']
TestLinks = ['Link_A', 'Link_B']
#TestCourses =

class FpMock:
    class configClass:
        
        data = { 'FLATPAGES_AUTO_RELOAD': True, 'FLATPAGES_EXTENSION': '.md', 
                'FLATPAGES_ROOT': '.' }
        
        def setdefault(self, key, val):
            if key in self.data.keys():
                return
            self.data[key] = val
            print "key: %s, val:%s"%(key,self.data[key] )
            return
    
        def __getitem__(self, key):
            return self.data[key]
        
    @property
    def config(self):
        return self.configClass()

    def before_request( self, conditional_auto_reset):
        return DataDir
    
    @property 
    def root_path(self):
        return DataDir


class Test(unittest.TestCase):


    def testLocalFiles(self):
        data = LocalData( DataDir, FpInst = FpMock() )
        self.assertEqual( data.getCourses( TestSemesters[0] ), TestCourses1 )
        self.assertEqual( data.getSemesters(), TestSemesters )
        self.assertEqual( data.getLinks(), TestLinks )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLocalFiles']
    unittest.main()