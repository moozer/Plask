'''
Created on Jun 28, 2013

@author: moz
'''
import os

class LocalData(object):
    '''
    classdocs
    '''


    def __init__(self, DataDir):
        '''
        Constructor
        '''
        self.DataDir = DataDir

    
    def getCourses( self,  semester = None ):
        ''' @returns the list of course in a given semester (based on directories) '''
        if not semester:
            return None
        
        Courses = [ c for c in os.listdir("%s/%s"%(self.DataDir, semester)) if os.path.isdir("%s/%s/%s"%(self.DataDir, semester,c))]
        return Courses

    def getSemesters( self ):
        ''' @returns the list of semesters (based on directories) '''    
        semesters = [ c for c in os.listdir(self.DataDir) if os.path.isdir("%s/%s"%(self.DataDir, c))]
        return semesters
    
    