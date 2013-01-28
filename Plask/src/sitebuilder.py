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

coursesections = ['Introduction', 'Teaching goals', 'Learning goals', 
                  'Evaluation', 'Literature', 'Exam questions', 'Schedule']

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
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
    
    Courses = [ c for c in os.listdir("pages/%s"%semester) if os.path.isdir("pages/%s/%s"%(semester,c))]
    return Courses

def getSemesters():
    ''' @returns the list of semesters (based on directories) '''    
    semesters = [ c for c in os.listdir("pages/") if os.path.isdir("pages/%s"%c)]
    return semesters

def getLinks():
    ''' @returns the list of top level pages aka. links (based on directories) '''    
    linkspages = [page for page in pages if page.path.split('/').__len__() < 2]
    return linkspages

def getHandinList( filename ):
    ''' from a hand-in csv file, return the list of hand-ins. 
        Columns: Date (YYMMDD), Hand-in, Comment
    '''
    print >> sys.stderr, filename
    try:
        reader = csv.DictReader(open(filename, 'r'), delimiter='\t')
    except IOError:
        return []

    handinlist =[]
    for entry in reader:
        for datestring in entry['Date'].split(','):
            date = datetime.datetime.strptime( datestring, "%y%m%d")
            print >> sys.stderr,  date
            handin = {  'Date': date, 'Datestring': datetime.datetime.strftime( date,"%d/%m-%y" ),
                        'Handin': entry['Hand-in'], 'Comment': entry['Comment']}
            handinlist.append( handin )
        
    return handinlist

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
    if not os.path.isdir("pages/"+dirname):
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
    schedule = getScheduleList( "pages/" + dirname + "/schedule.csv" )
    handins = getHandinList( "pages/"+dirname+"/handins.csv" )

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


@app.route('/ics/')
@app.route('/ics/<string:filename>')
@app.route('/ics/<string:filename>.ics')
def calendar(filename = "nonexist"):
    print >> sys.stderr, "filename: %s"%filename
    
    parts = filename.split(' ')
    print >>sys.stderr, "parts:", parts
    if len(parts) < 2:
        return render_template('icsindex.html', 
                      filename=filename, links=getLinks())
    
    semester = parts[0]
    course = ' '.join( parts[1:] )
    dirname = u"%s/%s"%(semester,course) 

    print >> sys.stderr, "sem; %s, course: %s, dirname: %s"%(semester, course, dirname)
    if not os.path.isdir("pages/"+dirname):
        abort( 404 )

    handins = getHandinList( "pages/"+dirname+"/handins.csv" )
    if len( handins ) == 0:
        abort( 404 ) # no data
    
    # build ics
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for handin in handins:
        event = Event()
        event.add('summary', "%s"%handin['Handin'])
        
        event.add('dtstart', handin['Date'].date())            
        event.add('description', handin['Comment'])            
    
        cal.add_component(event)
        
    return cal.to_ical()

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
        app.run(port=8000)
        
