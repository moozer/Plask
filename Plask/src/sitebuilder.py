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
# from icalendar import Calendar, Event
from Storage.LocalData import LocalData
from Storage.Calendars import HandinsCalendar
from Storage.Schedule import SemesterSchedule

# the list of sections in the course plan 
coursesections = ['Introduction', 'Teaching goals', 'Learning goals', 
                  'Evaluation', 'Literature', 'Exam questions', 'Schedule']
#LocalPageDir="../../../PlaskData/pages" # without trailing /
LocalPageDir="./testData" # without trailing /

# config options
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
#FLATPAGES_ROOT = LocalPageDir
FREEZER_BASE_URL = "/Plask/"
FREEZER_DESTINATION = "/tmp/Plask/"

if len(sys.argv) > 1:
    FLATPAGES_ROOT = sys.argv[1]
else:
    FLATPAGES_ROOT = LocalPageDir

data = LocalData( FLATPAGES_ROOT )
hical = HandinsCalendar( data )

# basic flask object
app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)



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
    links = [pages.get(l) for l in data.getLinks()] 

    if not course or not semester:
        return render_template('fagplanindex.html', 
                        semesters=data.getSemesters(), semester=semester, 
                        courses=data.getCourses( semester ), links=links )
    
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
    handins = hical.getHandinList( semester,course )

    return render_template('fagplan.html', schedule=schedule, handins=handins,
                           course=course, semester=semester, 
                           pages=basepages, coursesections=coursesections, 
                           links=links, sectionpages=sectionpages)

@app.route('/overview/')
@app.route('/overview/<string:semester>/')
@app.route('/overview/<string:semester>/<string:overview>/')
@app.route('/overview/<string:semester>/<string:overview>.html')
def overview(overview = None, semester = None):
    if semester:
        if not semester in data.getSemesters():
            semester = None
    
    links = [pages.get(l) for l in data.getLinks()] 

    if not overview or not semester:
        return render_template('overviewindex.html', 
                      semesters=data.getSemesters(), semester=semester, 
                      coursesections=coursesections, links=links)

    basepages = [p for p in pages if overview in p.meta.get('sectionname', []) and semester in p.path ]
    return render_template('overview.html', semester=semester, 
                           pages=basepages, overview=overview,
                           links=links)

@app.route('/ics/')
@app.route('/ics/<string:filename>')
@app.route('/ics/<string:filename>.ics')
def calendar(filename = "nonexist"):
    # no cs requested
    links = [pages.get(l) for l in data.getLinks()] 
    if filename == "nonexist":
        return render_template('icsindex.html', 
                      filename=filename, links=links)
    
    parts = filename.split(' ')

    # part 1 is the semester
    if not parts[0] in data.getSemesters():
        abort( 404 )
    semester = parts[0]
    
    # semester only?
    if len(parts) == 1:
        return hical.getSemesterIcs(semester)    
    else:    
        semester = parts[0]
        course = ' '.join( parts[1:] )
        dirname = u"%s/%s"%(semester,course) 
    
        if not os.path.isdir("%s/%s"%(LocalPageDir, dirname)):
            abort( 404 )
    
        return hical.getCourseIcs(semester, course)

@app.route('/')
@app.route('/<path:path>/')
def page(path = "index"):
    page = pages.get_or_404(path)
    links = [pages.get(l) for l in data.getLinks()] 
    return render_template('page.html', page=page, 
                           pages=pages, links=links)
    

@app.route('/semesterplan')
@app.route('/semesterplan/')
@app.route('/semesterplan/<string:semester>')
@app.route('/semesterplan/<string:semester>/')
def semesterplanlist():
    ''' semesterplan list if not supplied both class and semester '''
    links = [pages.get(l) for l in data.getLinks()] 
    semesters = data.getAllClasses()    
    title = "Semester list"

    return render_template('semesterplanlist.html', page=page, 
                           pages=pages, links=links, title = title,
                           semesters = semesters )
    

@app.route('/semesterplan/<string:semester>/<string:classname>')
def semesterplan( semester, classname ):
    ''' semesterplan based on semester+class combo '''
    links = [pages.get(l) for l in data.getLinks()] 
    s = SemesterSchedule( data ).getList( semester, classname )
    
    sem_intro = pages.get('%s/%s/Introduction'%(semester, classname) )
    sem_eval = pages.get('%s/%s/Evaluation'%(semester, classname) )
    sem_contacts = pages.get('%s/%s/Contacts'%(semester, classname) )
    
    courselist = data.getCourses( semester, classname )
    title = "Semesterplan - %s - %s"%( classname, semester)
    
    return render_template('semesterplan.html', page=page, 
                           pages=pages, schedule=s, links=links, weeks=[35,43],
                           sem_intro = sem_intro, sem_eval = sem_eval, sem_contacts = sem_contacts,
                           courses = courselist, semester = semester, classname=classname, title = title)
  
# --------
if __name__ == '__main__':
    # are building static pages?
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()

#         Cmd = "ncftpput -f '../ittech.cfg' -R -m '/PlaskSrc' '.'"
#         os.system(Cmd)
#         Cmd = "ncftpput -f '../ittech.cfg' -R -m '.' '%s'"%(FREEZER_DESTINATION)
#         os.system(Cmd)
#        
#         print "Data is now available on http://ittech.eal.dk%s"%FREEZER_BASE_URL
        exit()
    
    app.run(host='0.0.0.0', port=8000)

