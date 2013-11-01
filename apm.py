import os, requests

def mkdir(name):
  if not os.path.exists(name):
    os.makedirs(name)

def init(name='devops'):
  mkdir(name)
  # Touch hosts, site.yml
  open(name + '/production', 'a')
  open(name + '/staging', 'a')
  open(name + '/site.yml', 'a')
  # mkdir roles, group_vars, host_vars
  mkdir(name + '/roles')
  mkdir(name + '/group_vars')
  mkdir(name + '/host_vars')
  generate(name + '/roles/common', 'role')

def generate(name, category='role'):
  if category is 'role':
    mkdir(name)
    mkdir(name + '/files')
    mkdir(name + '/handlers')
    mkdir(name + '/tasks')
    open(name + '/tasks/main.yml', 'a')
    mkdir(name + '/templates')
    mkdir(name + '/vars')

