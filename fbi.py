#!/usr/bin/env python

###
# Simple Fogbugz Interpreter
###

import cmd
import ConfigParser
import getpass
import os
import readline
import sys

from FogBugzPy.fogbugz import FogBugz


class FogbugzInterpreter(cmd.Cmd):
  '''
  Commands:
    list
    filter
    edit/update
    add/new
    [#xxx]
  '''

  def __init__(self, configfile=os.path.expanduser('~/.fbi')):
    # Load config
    self.CONFIG_FILE = configfile
    self.config = ConfigParser.SafeConfigParser()
    self.config.read(self.CONFIG_FILE)

    try:
      self.url = self.config.get('main', 'url')
      self.token = self.config.get('main', 'token')
      self.fb = FogBugz(self.url)
      self.fb._token = self.token
    except:
      sys.stdout.write('FogBugz URL: ')
      self.url = sys.stdin.readline().strip()
      sys.stdout.write('Email: ')
      email = sys.stdin.readline().strip()
      password = getpass.getpass('Password: ')
      self.fb = FogBugz(self.url)
      try:
        self.fb.logon(email, password)
      except Exception, e:
        print "ERROR:", e
        sys.exit()
      self.token = self.fb._token

      # Write Config
      try:
        self.config.add_section('main')
      except:
        pass
      self.config.set('main', 'url', self.url)
      self.config.set('main', 'token', self.token)
      self.config.write(open(self.CONFIG_FILE, 'wb'))

    cmd.Cmd.__init__(self)
    self.prompt = 'fbi> '
    pass

  def do_greet(self, line):
    print 'hello'

  '''

  API Details:
  http://fogbugz.stackexchange.com/fogbugz-xml-api

  * Get filters
  * Get Projects
  * Get Areas

  * search for specific items

  * Build Child Trees + Views

  100 Item Number
  +-101 Test
    +-103 Sub2
      +-102 Sub3
    +-104 Sub2

  Update estimate
  Update due date
  
  Start time
  End time

  '''

  def do_list(self, line):
    # Default Filter

    # r = self.fb.search(cols='sTitle,latestEvent')

    r = self.fb.search(q=384, cols='ixBug,ixBugParent,ixBugChildren,fOpen,sTitle,ixProject,sProject,ixArea,sArea,ixStatus,sStatus,ixPriority,sPriority,hrsCurrEst,hrsElapsed,ixCategory,sCategory,dtDue')

    if r.description is not None:
      print 'Filter:', r.description.string
      print

    for case in r.findAll('case'):
      print case['ixbug'].rjust(8), case.stitle.string
      print case
      # print "    ", case.events.event.evtdescription.string
      print

    # list items
    pass

  def do_search(self, line):
    # search items
    pass
  
  def do_EOF(self, line):
    print 'Exiting'
    sys.exit()


if __name__ == '__main__':
  FogbugzInterpreter().cmdloop()



'''
# Alternate implementation that extends Python console
import atexit
import code

class FogBugzInteractiveConsole(code.InteractiveConsole):
  def __init__(self, locals=None, filename='<console>', 
               config=os.path.expanduser('~/.fbi')):
    # Load Config

    code.InteractiveConsole.__init__(self, locals, filename) 

    # History!
    histfile = os.path.expanduser('~/.fbi_history')
    self.init_history(histfile)


  def init_history(self, histfile):
    readline.parse_and_bind("tab: complete")
    if hasattr(readline, "read_history_file"):
      try:
        readline.read_history_file(histfile)
      except IOError:
        pass
      atexit.register(self.save_history, histfile)


  def save_history(self, histfile):
    readline.write_history_file(histfile)
'''

