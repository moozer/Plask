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
    
    def getList(self, semester, classname ):
        ''' parses the semester schedule csv file and returns the entries.
            preserves the order of the csv
            @return: iterable dictationary of entries
        '''
        filename = "%s/%s/%s"%( semester, classname, self.schedulefile )
        
        try:
            reader = csv.DictReader( self.data.getFile( filename ), delimiter='\t')
        except IOError:
            return []
        
        entries = []
        for line in reader:
            try:
                WeekList = {}
                for week in self._rangeexpand( line['Weeks']):
                    WeekList[week] = int(line['Lessons'])
    
                entry = {   'Course': line['Course'], 'Teacher': line['Teacher'], 
                            'ECTS': float(line['ECTS']), 'Lessons': WeekList, 'Link': line['Link']}
    
                if len(entries) > 0:
                    lastEntry = entries[-1]
                    if      lastEntry['Teacher'] == entry['Teacher'] \
                        and lastEntry['Course'] == entry['Course'] \
                        and lastEntry['ECTS'] == entry['ECTS']:
                        lastEntry['Lessons'].update(WeekList)
                        
                        # handle differences in "Link" column
                        # just use the biggest string
                        if entry['Link'] > lastEntry['Link']:
                            lastEntry['Link'] = entry['Link']
                        continue
            except KeyError, e:
                raise KeyError( "%s malformed, missing column: %s"%(filename, e))
            entries.append( entry )
        
        return entries
        
        
          