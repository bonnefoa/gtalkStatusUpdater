#!/usr/bin/env python
import sys
import time
from datetime import * 
from xmpp import * 
import random

USERNAME = "t"
PASSWORD = "t"
RESOURCE = "gmail.com"
stat_prefix = "s"
stat_suffix = ".....@_\""
mu_delay = 60 
sigma_delay = 10
dest = datetime(year=2010, month= 9,day=03, hour=17, minute=30)

def connect():
  cl=Client(server='gmail.com',debug=[])
  cl.connect() 
  if not cl.auth(USERNAME, PASSWORD, RESOURCE):
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

cl = connect()

step(cl)

cl.disconnect()

