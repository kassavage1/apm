import os, requests

def mkdir(name):
  if not os.path.exists(os.getcwd() + '/' + name):
    os.makedirs(os.getcwd() + '/' + name)

def touch(name):
  open(os.getcwd() + '/' + name, 'a')

def init(name='devops'):
  mkdir(name)
  # Touch hosts, site.yml
  touch(name + '/production')
  touch(name + '/staging')
  touch(name + '/site.yml')
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
    touch(name + '/tasks/main.yml')
    mkdir(name + '/templates')
    mkdir(name + '/vars')

