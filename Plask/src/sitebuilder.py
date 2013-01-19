'''
Created on 17 Jan 2013

@author: moz
'''

from flask import Flask, render_template, abort
from flask_flatpages import FlatPages
import sys, os
from flask_frozen import Freezer
import csv

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FREEZER_BASE_URL = "/Plask/"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

def getCourses( semester = None ):
    if not semester:
        return None
    
    Courses = [ c for c in os.listdir("pages/%s"%semester) if os.path.isdir("pages/%s/%s"%(semester,c))]
    return Courses

def getSemesters():
    semesters = [ c for c in os.listdir("pages/") if os.path.isdir("pages/%s"%c)]
    return semesters

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/fagplan/')
@app.route('/fagplan/<string:semester>/')
@app.route('/fagplan/<string:semester>/<string:course>/')
@app.route('/fagplan/<string:semester>/<string:course>.html')
def fagplan(course = None, semester = None):
    if not course or not semester:
        return render_template('fagplanindex.html', 
                        semesters=getSemesters(), semester=semester, 
                        courses=getCourses( semester ))

    
    dirname = u"%s/%s"%(semester,course) 
    if not os.path.isdir("pages/"+dirname):
        abort( 404 )
        
    # for the content text
    basepages = [p for p in pages if dirname == os.path.dirname(p.path)]
    # for the schedule
    reader = csv.DictReader(open("pages/"+dirname+"/schedule.csv", 'r'), delimiter='\t')
    schedule = [ entry for entry in reader]
    return render_template('fagplan.html', schedule=schedule, course=course, semester=semester, pages=basepages)

@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
#        semester = "2013S"
#        course = "ITT2 Networking"    
#        dirname = u"%s/%s"%(semester,course)
#        print pages
#        basepages = [p for p in pages if dirname == os.path.dirname(p.path)]
#        print basepages
#        fagplan("ITT2 Networking", "2013S")
        #fagplan()
        app.run(port=8000)
        
