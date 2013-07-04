'''
Created on Jul 4, 2013

@author: moz
'''

from flask_frozen import Freezer
from flask import redirect

from sitebuilder import app

FREEZER_BASE_URL = "/Plask/"
FREEZER_DESTINATION = "/tmp/Plask/"

# adding route for freezer base url to handle lnks in .md files properly
@app.route(FREEZER_BASE_URL+'<path:path>/')
def freeze_base_url(path):
    return redirect( path, 301 )



if __name__ == '__main__':
    freezer = Freezer(app)
    freezer.freeze()

#         Cmd = "ncftpput -f '../ittech.cfg' -R -m '/PlaskSrc' '.'"
#         os.system(Cmd)
#         Cmd = "ncftpput -f '../ittech.cfg' -R -m '.' '%s'"%(FREEZER_DESTINATION)
#         os.system(Cmd)
#        
#         print "Data is now available on http://ittech.eal.dk%s"%FREEZER_BASE_URL
#         exit()