#!/usr/bin/python

'''
Created on 17 Jan 2013

@author: moz
'''

from flask import Flask, render_template, abort, redirect
from flask_flatpages import FlatPages
import sys, os
from flask_frozen import Freezer
import csv
import datetime
from icalendar import Calendar, Event

# the list of sections in the course plan 
coursesections = ['Introduction', 'Teaching goals', 'Learning goals', 
                  'Evaluation', 'Literature', 'Exam questions', 'Schedule']
LocalPageDir="../../../PlaskData/pages" # without trailing /


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = LocalPageDir
FREEZER_BASE_URL = "/Plask/"
FREEZER_DESTINATION = "/tmp/Plask/"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

def getCourses( semester = None ):
    ''' @returns the list of course in a given semester (based on directories) '''
    if not semester:
        return None
    
    Courses = [ c for c in os.listdir("%s/%s"%(LocalPageDir, semester)) if os.path.isdir("%s/%s/%s"%(LocalPageDir, semester,c))]
    return Courses

def getSemesters():
    ''' @returns the list of semesters (based on directories) '''    
    semesters = [ c for c in os.listdir(LocalPageDir) if os.path.isdir("%s/%s"%(LocalPageDir, c))]
    return semesters

def getLinks():
    ''' @returns the list of top level pages aka. links (based on directories) '''    
    linkspages = [page for page in pages if page.path.split('/').__len__() < 2]
    return linkspages

def getHandinList( semester, course, prefix="" ):
    ''' from a hand-in csv file, return the list of hand-ins. 
        Columns: Date (YYMMDD), Hand-in, Comment
    '''
    filename = "%s/%s/%s/handins.csv"%(LocalPageDir, semester,course)    
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

def getHandinsListSemester( semester ):
    ''' returns the aggregated list of all handins from the semester '''
    if not semester in getSemesters():
        return []
    
    HiList = []
    for course in getCourses( semester ):
        HiList.extend( getHandinList( semester, course, prefix="%s: "%course ) )
    
    return HiList

def getScheduleList(filename):
    reader = csv.DictReader(open( filename, 'r'), delimiter='\t')
    schedule = [entry for entry in reader]
    return schedule


# adding route for freezer base url to handle lnks in .md files properly
@app.route(FREEZER_BASE_URL+'<path:path>/')
def freeze_base_url(path):
    return redirect( path, 301 )

@app.route('/fagplan/')
@app.route('/fagplan/<string:semester>/')
@app.route('/fagplan/<string:semester>/<string:course>/')
@app.route('/fagplan/<string:semester>/<string:course>.html')
def fagplan(course = None, semester = None):
    if not course or not semester:
        return render_template('fagplanindex.html', 
                        semesters=getSemesters(), semester=semester, 
                        courses=getCourses( semester ), links=getLinks())
    
    dirname = u"%s/%s"%(semester,course) 
    if not os.path.isdir("%s/%s"%(LocalPageDir, dirname)):
        abort( 404 )
         
    # for the content text
    basepages = [p for p in pages if dirname == os.path.dirname(p.path)]
    sectionpages = {}
    for s in coursesections:
        for p in basepages:
            if s in p.path:
                sectionpages[s] = p
                break

    # for the schedule
    schedule = getScheduleList( "%s/%s/%s"%(LocalPageDir, dirname, "schedule.csv") )
    handins = getHandinList( semester,course )

    return render_template('fagplan.html', schedule=schedule, handins=handins,
                           course=course, semester=semester, 
                           pages=basepages, coursesections=coursesections, 
                           links=getLinks(), sectionpages=sectionpages)

@app.route('/overview/')
@app.route('/overview/<string:semester>/')
@app.route('/overview/<string:semester>/<string:overview>/')
@app.route('/overview/<string:semester>/<string:overview>.html')
def overview(overview = None, semester = None):
    if semester:
        if not semester in getSemesters():
            semester = None
    
    if not overview or not semester:
        return render_template('overviewindex.html', 
                      semesters=getSemesters(), semester=semester, 
                      coursesections=coursesections, links=getLinks())

    basepages = [p for p in pages if overview in p.meta.get('sectionname', []) and semester in p.path ]
    return render_template('overview.html', semester=semester, 
                           pages=basepages, overview=overview,
                           links=getLinks())

def GenerateIcs(handins):
    # build ics
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    for handin in handins:
        event = Event()
        event.add('summary', handin['Handin'])
        event.add('dtstart', handin['Date'].date())
        event.add('description', handin['Comment'])
        cal.add_component(event)
    
    retval = cal.to_ical()
    return retval

@app.route('/ics/')
@app.route('/ics/<string:filename>')
@app.route('/ics/<string:filename>.ics')
def calendar(filename = "nonexist"):
    # no cs requested
    if filename == "nonexist":
        return render_template('icsindex.html', 
                      filename=filename, links=getLinks())
    
    parts = filename.split(' ')

    # part 1 is the semester
    if not parts[0] in getSemesters():
        abort( 404 )
    semester = parts[0]
    
    # semester only?
    if len(parts) == 1:
        handins = getHandinsListSemester(semester)
    else:    
        semester = parts[0]
        course = ' '.join( parts[1:] )
        dirname = u"%s/%s"%(semester,course) 
    
        if not os.path.isdir("%s/%s"%(LocalPageDir, dirname)):
            abort( 404 )
    
        handins = getHandinList( semester,course )

    if len( handins ) == 0:
        abort( 404 ) # no data
    
    return GenerateIcs(handins)

@app.route('/')
@app.route('/<path:path>/')
def page(path = "index"):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page, 
                           pages=pages, links=getLinks())
    
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()

        Cmd = "ncftpput -f '../ittech.cfg' -R -m '/PlaskSrc' '.'"
        os.system(Cmd)
        Cmd = "ncftpput -f '../ittech.cfg' -R -m '.' '%s'"%(FREEZER_DESTINATION)
        os.system(Cmd)
        
        print "Data is now available on http://ittech.eal.dk%s"%FREEZER_BASE_URL
        
    else:
        app.run(host='0.0.0.0', port=8000)

