#!/usr/bin/env python
import sys,os,time
from datetime import * 
from xmpp import * 
import random

RESOURCE = "gmail.com"
stat_prefix = "s"
stat_suffix = ".....@_\""
mu_delay = 60 
sigma_delay = 10
dest = datetime(year=2010, month= 9,day=03, hour=17, minute=30)

def readConfigFile():
  jidparams = {}
  if os.access(os.environ['HOME']+'/.xsend',os.R_OK):
        for ln in open(os.environ['HOME']+'/.xsend').readlines():
            key,val=ln.strip().split('=',1)
            jidparams[key.lower()]=val
        return jidparams
  for mandatory in ['jid','password']:
      if mandatory not in jidparams.keys():
           open(os.environ['HOME']+'/.xsend','w').write('#JID=romeo@montague.net\n#PASSWORD=juliet\n')
           print 'Please ensure the ~/.xsend file has valid JID for sending messages.'
           sys.exit(0)

def connect(jidparams):
  jid=protocol.JID(jidparams['jid'])
  #cl=Client(server=jid.getDomain(),proxy = {'host':'proxy.my.net','port':8080,'user':'me','password':'secret'},debug=[])
  cl=Client(server=jid.getDomain(),debug=[])
  cl.connect() 
  if not cl.auth(jid.getNode(),jidparams['password'], RESOURCE):
      raise IOError('Can not auth with server.')
  return cl

def setStatus(client, status):
  cl.send(Iq('set','google:shared-status', payload=[
		Node('show',payload=["default"]),
		Node('status',payload=[status] )
  ]))

def total_seconds(td):
  secNum = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 
  return secNum 

def getDif(dest):
  cur = dest.today()
  diff = cur - dest
  return total_seconds ( diff )

def format_message():
  sec = getDif(dest)
  return stat_prefix + str(sec) + stat_suffix

def step(cl):
  delay = random.gauss(mu_delay, sigma_delay)
  print "sleeping for " + str(delay)
  time.sleep(delay)
  setStatus(cl, format_message() )
  step(cl)

jidparams = readConfigFile()
cl = connect(jidparams)

step(cl)

cl.disconnect()

