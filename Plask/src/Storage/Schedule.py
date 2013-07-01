'''
Created on Jul 1, 2013

@author: moz

links:
- range expander: http://rosettacode.org/wiki/Range_expansion#Python
'''
import csv

class SemesterSchedule(object):
    '''
    classdocs
    '''
    schedulefile = "SemesterSchedule.csv"

    def __init__(self, data):
        '''
        Constructor
        '''
        self.data = data

    def _rangeexpand(self, txt):
        ''' txt contains numbers and ranges, e.g. 3-7,8,7
            @return: the complete list of integers covered b txt
        '''
        lst = []
        for r in txt.split(','):
            if '-' in r[1:]:
                r0, r1 = r[1:].split('-', 1)
                lst += range(int(r[0] + r0), int(r1) + 1)
            else:
                lst.append(int(r))
        return lst
    
    def getList(self, semester ):
        ''' parses the semester schedule csv file and returns the entries.
            @return: iterable dictationary of entries
        '''
        filename = "%s/%s"%( semester, self.schedulefile )
        reader = csv.DictReader( self.data.getFile( filename ), delimiter='\t')
        
        entries = []
        for line in reader:
            WeekList = {}
            for week in self._rangeexpand( line['Weeks']):
                WeekList[week] = int(line['Lessons'])

            entry = {   'Course': line['Course'], 'Teacher': line['Teacher'], 
                        'ECTS': float(line['ECTS']), 'Lessons': WeekList }
            entries.append( entry )
        
        return entries
        
        
          