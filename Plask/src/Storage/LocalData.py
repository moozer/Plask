'''
Created on Jun 28, 2013

@author: moz
'''
import os
#from flask_flatpages import FlatPages
#import flask_flatpages
import glob



class LocalData(object):
    '''
    classdocs
    '''


    def __init__(self, DataDir ):
        '''
        Constructor
        '''
        self.DataDir = DataDir
    
    def getCourses( self,  semester = None, classname = None ):
        ''' @returns the list of course in a given semester (based on directories) '''

        if semester and classname:
            Courses = [ c for c in os.listdir("%s/%s/%s"%(self.DataDir, semester, classname)) if os.path.isdir("%s/%s/%s/%s"%(self.DataDir, semester, classname,c))]
            return { semester: { classname: Courses}}

        if semester:
            retval = {}

            for classname in self.getClasses( semester )[semester]:
                retval.update( self.getCourses( semester, classname )[semester] )
            return {semester: retval}
        
        retval = {}
        for semester in self.getSemesters():
            retval.update(  self.getCourses( semester ) )
        return retval
        
    def getClasses(self, semester=None ):
        ''' @returns the list of classes in a given semester (based on directories) 
            if semester is none - all semesters are returned
        '''        
        if semester:
            Classes = [ c for c in os.listdir("%s/%s"%(self.DataDir, semester)) if os.path.isdir("%s/%s/%s"%(self.DataDir, semester, c))]
            return { semester: Classes }

        retval = {}
        for sem in self.getSemesters():
            retval.update( self.getClasses(sem))
        
        return retval


    def getSemesters( self ):
        ''' @returns the list of semesters (based on directories) '''    
        semesters = [ c for c in os.listdir(self.DataDir) if os.path.isdir("%s/%s"%(self.DataDir, c))]
        return semesters

    def getLinks( self ):
        ''' @returns the list of top level pages aka. links (based on directories) '''  
        files = glob.glob("%s/%s"%(self.DataDir, '*.md') )
        listnames = ['.'.join(os.path.basename(l).split('.')[:-1]) for l in files]
        return sorted(listnames)
    
    def getFile( self, filename ):
        ''' opens a filepointer to a file relative to self.DataDir '''
        fullpath = os.path.join( self.DataDir, filename )
        return open( fullpath, "r")

