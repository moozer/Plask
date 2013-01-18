'''
Created on 17 Jan 2013

@author: moz
'''

from flask import Flask, render_template, abort
from flask_flatpages import FlatPages
import sys, os
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/tag/<string:tag>/')
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return render_template('tag.html', pages=tagged, tag=tag)

@app.route('/fagplan/<string:semester>/<string:course>')
def fagplan(course, semester):
    dirname = u"%s/%s"%(semester,course) 
    print dirname
    if not os.path.isdir("pages/"+dirname):
        abort( 404 )
           
    basepages = [p for p in pages if dirname == os.path.dirname(p.path)]
    return render_template('fagplan.html', course=course, semester=semester, pages=basepages)


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
        #fagplan("ITT2 Networking", "2013S")
        app.run(port=8000)
        
