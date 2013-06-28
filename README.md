Plask
=====

Course planning software

How to use
----------

1. mkdir LocalDir

2. cd LocalDir

2. git clone https://github.com/moozer/Plask.git
  This will pull all the code in a readonly fashion
  
3. git clone git@github.com:moozer/PlaskData.git
  This will pull the data in a read/write fashion. You must be a contributor to do this. 
  If you are not, do your own fork, and use the appropriate URL

4. cd Plask/Plask/src

5. You have two options for its use

  a. *python sitebuilder.py*
  
    This will most likely complain about missing libraries. They must be installed for this to work.
  
    When it work, it is accessible on http://localhost:8000

  b. *python sitebuilder.py build*
  
    This will create the static html pages and upload them to a server. the program ncftp must be installed.
  
    Also, a credentials file at LocalDir/Plask/Plask/ittech.cfg must be made. 
    See [ncftpput -f XX](http://ncftp.com/ncftp/doc/ncftpput.html) for format. 
  
Issues
------

As with all software, this code is flawless. If you find any odd *features*, create an issue associated 
to the project [on github](https://github.com/moozer/Plask/issues)
