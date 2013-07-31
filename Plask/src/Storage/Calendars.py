'''
Created on Jun 28, 2013

@author: moz
'''
import datetime
import csv
import icalendar

class HandinsCalendar(object):
    '''
    classdocs
    '''


    def __init__(self, DataObject ):
        '''
        Constructor
        '''
        self.data = DataObject

    
    def getHandinList( self, semester, classname, course, prefix="" ):
        ''' from a hand-in csv file, return the list of hand-ins. 
            Columns: Date (YYMMDD), Hand-in, Comment
        '''
        filename = "%s/%s/%s/handins.csv"%( semester, classname, course )
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

    
    def getHandinsListSemester(self, semester, classname ):
        ''' returns the aggregated list of all handins from the semester '''        
        if not semester in self.data.getSemesters():
            return []

        if not classname in self.data.getClasses( semester ):
            return []
         
        HiList = []
        for course in self.data.getCourses( semester, classname ):
            HiList.extend( self.getHandinList( semester, classname, course, prefix="%s: "%course ) )
         
        return HiList
        

    def _GenerateHandinIcs(self, Handins):
        # build ics
        cal = icalendar.Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')
        for handin in Handins:
            event = icalendar.Event()
            event.add('summary', handin['Handin'])
            event.add('dtstart', handin['Date'].date())
            event.add('description', handin['Comment'])
            cal.add_component(event)
        
        retval = cal.to_ical()
        return retval

    def getCourseIcs(self, semester, classname, course ):
        ''' returns an ics file based on the handins of a course'''
        hi = self.getHandinList( semester, classname, course )
        return self._GenerateHandinIcs(hi)
         
    
    def getSemesterIcs(self, semester, classname):
        ''' returns an ics file based on the handins of a semester'''
        hi = self.getHandinsListSemester( semester, classname )
        return self._GenerateHandinIcs(hi)

        
    
    
