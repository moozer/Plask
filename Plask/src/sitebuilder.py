#!/usr/bin/python

'''
Created on 17 Jan 2013

@author: moz
'''

from flask import Flask, render_template, redirect
from flask_flatpages import FlatPages
import sys, os
import csv

from Storage.LocalData import LocalData
from Storage.Calendars import HandinsCalendar
from Storage.Schedule import SemesterSchedule

# the list of sections in the course plan 
coursesections = ['Introduction', 'Teaching goals', 'Learning goals', 
                  'Evaluation', 'Literature', 'Exam questions', 'Schedule']

#LocalPageDir="./testData" # without trailing /

class base_conf:
    # config options
    DEBUG = True
    #DEBUG = False
    FLATPAGES_AUTO_RELOAD = DEBUG
    FLATPAGES_EXTENSION = '.md'
    
    if len(sys.argv) > 1:
        FLATPAGES_ROOT = sys.argv[1]
    else:
        FLATPAGES_ROOT = "./testData" # without trailing /


data = LocalData( base_conf.FLATPAGES_ROOT )
hical = HandinsCalendar( data )

# basic flask object
app = Flask(__name__)
app.config.from_object(base_conf)
pages = FlatPages(app)

def getScheduleList(filename):
    reader = csv.DictReader(open( filename, 'r'), delimiter='\t')
    schedule = [entry for entry in reader]
    return schedule

@app.route('/fagplan/')
@app.route('/fagplan/<string:semester>/')
def fagplanindex():
    ''' catch-all "fagplan" URL '''
    links = [pages.get(l) for l in data.getLinks()] 

    return render_template('fagplanindex.html', 
                        semesters=data.getClasses(),
                        classes=data.getClasses(), links=links )
   
@app.route('/fagplan/<string:semester>/<string:classname>/')
def fagplanlist( semester, classname):  
    links = [pages.get(l) for l in data.getLinks()] 
    courses = data.getCourses( semester, classname )[semester][classname]
    title = "Course list - %s - %s"%(semester, classname)
    
    return render_template('fagplanindex.html', 
                           courses=courses, semesters=data.getClasses(),
                           semester=semester, classname = classname,
                           links=links, title = title )
 
@app.route('/fagplan/<string:semester>/<string:classname>/<string:course>/')
def fagplan( semester, classname, course):
    links = [pages.get(l) for l in data.getLinks()] 
    
    # check if course plan is local
    allcoursesch = SemesterSchedule( data ).getList( semester, classname )
    coursesch = [c for c in allcoursesch if c['Course'] == course]
    
    if len( coursesch ) > 0:
        # just pick the first with the correct course name
        if coursesch[0]['Link'] != '.':
            return redirect( coursesch[0]['Link'] )
    # else just use the default build-in stuff
    
    dirname = u"%s/%s/%s"%(semester,classname, course) 
         
    title = "Course plan - %s - %s"%(semester, classname)
    
    # for the content text
    basepages = [p for p in pages if dirname == os.path.dirname(p.path)]
    sectionpages = {}
    for s in coursesections:
        for p in basepages:
            if s in p.path:
                sectionpages[s] = p
                break

    # for the schedule
    try:    
        schedule = getScheduleList( "%s/%s/%s"%(base_conf.FLATPAGES_ROOT, dirname, "schedule.csv") )
        handins = hical.getHandinList( semester, classname, course )
    except IOError:
        return render_template( 'NotFound.html' )

    return render_template('fagplan.html', schedule=schedule, handins=handins,
                           course=course, semester=semester, classname = classname,
                           pages=basepages, coursesections=coursesections, 
                           links=links, sectionpages=sectionpages, title = title )

@app.route('/overview/')
@app.route('/overview/<string:semester>/')
def overviewindex():
    links = [pages.get(l) for l in data.getLinks()] 

    return render_template('overviewindex.html', 
                  semesters=data.getClasses(), 
                  coursesections=coursesections, links=links)


@app.route('/overview/<string:semester>/<string:classname>/')
def overviewlist(semester, classname):
    links = [pages.get(l) for l in data.getLinks()] 
    return render_template('overviewindex.html', 
                    semesters=data.getClasses(), 
                    semester=semester, classname=classname,
                    coursesections=coursesections, links=links)



@app.route('/overview/<string:semester>/<string:classname>/<string:overview>/')
def overview(overview, semester, classname):
    links = [pages.get(l) for l in data.getLinks()]
    
    dirname = u"%s/%s"%(semester,classname)
    courses = data.getCourses( semester, classname )[semester][classname]
    
    for i,name in enumerate(coursesections):
        if name == overview:
            overviewname = "%02d_%s"%(i+1, name)
            break
        
    ovpages =  ["%s/%s/%s"%(dirname, c, overviewname) for c in courses]
    basepages = [pages.get( p ) for p in ovpages if pages.get(p) is not None]

    return render_template('overview.html', semester=semester, classname=classname,
                           pages=basepages, overview=overview,
                           links=links)

@app.route('/ics/')
def calendar(filename = "nonexist"):
    # no cs requested
    links = [pages.get(l) for l in data.getLinks()] 
    return render_template('icsindex.html',
                      filename=filename, links=links)
    
@app.route('/ics/<string:semester>/<string:classname>/schedule.ics')
def calendar_semester( semester, classname ):
    return hical.getSemesterIcs(semester, classname)
    
@app.route('/ics/<string:semester>/<string:classname>/<string:course>/schedule.ics')
def calendar_course( semester, classname, course ):
    return hical.getCourseIcs( semester, classname, course )
    
@app.route('/')
@app.route('/<path:path>/')
def page(path = "index"):
    page = pages.get_or_404(path)
    links = [pages.get(l) for l in data.getLinks()] 
    return render_template('page.html', page=page, 
                           pages=pages, links=links)
    

@app.route('/semesterplan/')
@app.route('/semesterplan/<string:semester>/')
def semesterplanlist():
    ''' semesterplan list if not supplied both class and semester '''
    links = [pages.get(l) for l in data.getLinks()] 
    semesters = data.getClasses()    
    title = "Semester list"

    return render_template('semesterplanlist.html', page=page, 
                           pages=pages, links=links, title = title,
                           semesters = semesters )
    

@app.route('/semesterplan/<string:semester>/<string:classname>/')
def semesterplan( semester, classname ):
    ''' semesterplan based on semester+class combo '''  
    links = [pages.get(l) for l in data.getLinks()] 
    s = SemesterSchedule( data ).getList( semester, classname )
    
    # @todo: this should be a list with all files in semester directory.
    sem_intro = pages.get('%s/%s/Introduction'%(semester, classname) )
    sem_eval = pages.get('%s/%s/Evaluation'%(semester, classname) )
    sem_contacts = pages.get('%s/%s/Contacts'%(semester, classname) )
    sem_literature = pages.get('%s/%s/Literature'%(semester, classname) )
    
    courselist = {c['Course']: c['Link']  for c in s}

    title = "Semesterplan - %s - %s"%( classname, semester)
    
    return render_template('semesterplan.html', page=page, 
                           pages=pages, schedule=s, links=links,
                           sem_intro = sem_intro, sem_eval = sem_eval, sem_contacts = sem_contacts,
                           sem_literature = sem_literature,
                           courses = courselist, semester = semester, classname=classname, title = title)
  
# --------
if __name__ == '__main__':   
    app.run(host='0.0.0.0', port=8000)

