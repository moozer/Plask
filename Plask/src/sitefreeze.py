'''
Created on Jul 4, 2013

@author: moz
'''


class freeze_conf:
    FREEZER_BASE_URL = "/Plask/"
    FREEZER_DESTINATION = "/tmp/Plask/"


from sitebuilder import app
from flask_frozen import Freezer
from flask import redirect
import os


# adding route for freezer base url to handle lnks in .md files properly
@app.route(freeze_conf.FREEZER_BASE_URL+'<path:path>/')
def freeze_base_url(path):
    return redirect( path, 301 )

app.config.from_object(freeze_conf)
freezer = Freezer(app)
freezer.freeze()

Cmd = "ncftpput -f '../ittech.cfg' -R -m '/PlaskSrc' '.'"
os.system(Cmd)
Cmd = "ncftpput -f '../ittech.cfg' -R -m '.' '%s'"%(freeze_conf.FREEZER_DESTINATION)
os.system(Cmd)

print "Data is now available on http://ittech.eal.dk%s"%freeze_conf.FREEZER_BASE_URL
