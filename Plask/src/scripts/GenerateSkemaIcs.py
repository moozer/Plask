'''
Created on 25 Jan 2013

@author: moz

Example from http://icalendar.readthedocs.org/en/latest/examples.html
>>> cal = Calendar()
>>> from datetime import datetime
>>> cal.add('prodid', '-//My calendar product//mxm.dk//')
>>> cal.add('version', '2.0')

>>> import pytz
>>> event = Event()
>>> event.add('summary', 'Python meeting about calendaring')
>>> event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=pytz.utc))
>>> event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
>>> event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))
>>> event['uid'] = '20050115T101010/27346262376@mxm.dk'
>>> event.add('priority', 5)

>>> cal.add_component(event)

>>> f = open('example.ics', 'wb')
>>> f.write(cal.to_ical())
>>> f.close()

'''
import csv
import datetime
from icalendar import Calendar, Event

# TODO: Make filename a command line parameter
filename = "Skema2013S.csv"

# 0 is all day
LessonHours = (([0,0], [23,59]), 
               ([8,30], [9,15]), ([9,15], [10,00]),
               ([10,20], [11,05]), ([11,05], [11,50]),
               ([12,30], [13,15]), ([13,15], [14,00]))


def iso_year_start(iso_year):
    ''' The gregorian calendar date of the first day of the given ISO year"
        from http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar 
    '''
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def iso_to_gregorian(iso_year, iso_week, iso_day):
    ''' Gregorian calendar date for the given ISO year, week and day
        from http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar
    '''
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)


def ReadSchedule( filename = filename, year = 2013 ):
    reader = csv.DictReader(open(filename, 'r'), delimiter='\t')

    lessonslist =[]
    for entry in reader:
        print entry
        
        for week in entry['Weeks'].split(','):
            for weekday in entry['Weekdays'].split(','):
                for lessons in entry['Lessons'].split(','):
                    date = iso_to_gregorian( year, int(week), int(weekday))
                    lessons = { 'Week': int( week ), 'Weekday': int(weekday), 'Lesson': int(lessons),
                                'Course': entry['Course'], 'Class': entry['Class'], 
                                'Teacher': entry['Teacher'], 'date': date}
                    lessonslist.append( lessons )
        
    return lessonslist


def WriteIcs(Schedule, Outfile = filename+'.ics'):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for lesson in Schedule:
        event = Event()
        event.add('summary', "%s: %s"%(lesson['Class'], lesson['Course']))
        hours = LessonHours[lesson['Lesson']][0][0]
        minutes = LessonHours[lesson['Lesson']][0][1]
        lessonstart  = datetime.datetime(lesson['date'].year, lesson['date'].month, lesson['date'].day )
        lessonstart += datetime.timedelta( hours=hours, minutes=minutes)
        event.add('dtstart', lessonstart)
        event.add('dtend', lessonstart+datetime.timedelta( minutes=45))
        #event.add('dtstamp', lesson['date'])
        #event['uid'] = '20050115T101010/27346262376@mxm.dk'
        #event.add('priority', 5)
    
        cal.add_component(event)
        
    f = open(Outfile, 'wb')
    f.write(cal.to_ical())
    f.close()
    print "Data output to %s"%Outfile


if __name__ == '__main__':
    Schedule = ReadSchedule()
    print "Number of lessons in Schedule: %d"%len(Schedule)
    WriteIcs( Schedule )
    pass

