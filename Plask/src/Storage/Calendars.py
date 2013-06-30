'''
Created on Jun 28, 2013

@author: moz
'''
import datetime
import csv

class HandinsCalendar(object):
    '''
    classdocs
    '''


    def __init__(self, DataObject ):
        '''
        Constructor
        '''
        self.data = DataObject

    
    def getHandinList( self, semester, course, prefix="" ):
        ''' from a hand-in csv file, return the list of hand-ins. 
            Columns: Date (YYMMDD), Hand-in, Comment
        '''
        filename = "%s/%s/handins.csv"%( semester,course )
        try:
            reader = csv.DictReader( self.data.getFile( filename ), delimiter='\t')
        except IOError:
            return []
    
        handinlist =[]
        for entry in reader:
            for datestring in entry['Date'].split(','):
                date = datetime.datetime.strptime( datestring, "%y%m%d")
                handin = {  'Date': date, 'Datestring': datetime.datetime.strftime( date,"%d/%m-%y" ),
                            'Handin': "%s%s"%(prefix,entry['Hand-in']), 'Comment': entry['Comment']}
                handinlist.append( handin )
            
        return handinlist

    
    def getHandinsListSemester(self, semester ):
        ''' returns the aggregated list of all handins from the semester '''        
        if not semester in self.data.getSemesters():
            return []
         
        HiList = []
        for course in self.data.getCourses( semester ):
            HiList.extend( self.getHandinList( semester, course, prefix="%s: "%course ) )
         
        return HiList
        
        
            