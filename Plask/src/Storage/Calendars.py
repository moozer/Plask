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


    def __init__(self, DataDir):
        '''
        Constructor
        '''
        self.DataDir = DataDir

    
    def getHandinList( self, semester, course, prefix="" ):
        ''' from a hand-in csv file, return the list of hand-ins. 
            Columns: Date (YYMMDD), Hand-in, Comment
        '''
        filename = "%s/%s/%s/handins.csv"%(self.DataDir, semester,course)    
        try:
            reader = csv.DictReader(open(filename, 'r'), delimiter='\t')
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
        
        
            