import os
import sys
import requests
import ConfigParser
import yaml
import tarfile

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

def signup(config, parser):
  if not parser.has_section('apm'):
    parser.add_section('apm')
  payload = {}
  payload['username'] = raw_input('Insert your username: ')
  payload['email'] = raw_input('Insert your email: ')
  payload['password'] = raw_input('Insert your password: ')
  r = requests.post('http://localhost:5000/user/', data=payload)
  if r.status_code == 200:
    for key, value in payload.items():
      parser.set('apm', key, value)
    parser.write(open(config, 'w+'))
  else:
    signup(config, parser)

def submit(config, parser):
  if len(parser.read(config)) is 0:
    signup(config, parser)
  if os.path.isfile(os.getcwd() + '/apm.yml'):
    data = yaml.load(open(os.getcwd() + '/apm.yml', 'r'))
    print data
    missingParams = []
    if not 'name' in data:
      missingParams.append('name')
    if not 'description' in data:
      missingParams.append('description')
    if not 'version' in data:
      missingParams.append('version')
    if len(missingParams) > 0:
      exit('Missing parameters: ', missingParams, 'in apm.yml file')
    data['username'] = parser.get('apm', 'username')
    data['author'] = data['username']
    data['password'] = parser.get('apm', 'password')
    tarname = os.getcwd() + '/' + data['name'] + '.tgz'
    tar = tarfile.open(tarname, 'w:gz')
    for filename in os.listdir(os.getcwd()):
      if filename is not '.git':
        tar.add(filename)
    tar.close()
    files = {'playbook': open(tarname, 'rb')}
    print data
    r = requests.post('http://localhost:5000/playbook', data=data, files=files)
    print r.text
  else:
    exit('No apm.yml file found in the current working directory')

def get():
  name = sys.argv[2]
  version = sys.argv[3] if len(sys.argv) == 4 else None
  url = 'http://localhost:5000/playbook/download/' + name
  if verion:
  url += 'version/' + version
  r = requests.get(url, stream=True)
  tarname = 'playbook.gz'
  with open(tarname, 'wb') as tar:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        tar.write(chunk)
        tar.flush()
  tar = tarfile.open(tarname, 'r:gz')
  mkdir(name)
  tar.extractall('./' + name)

def printMenu():
  exit('''You must include one of the following options:\n
  init - Will bootstrap a new folder with the prefered folder structure\n
  generate \'name\' - Generator for roles folder structure\n
  get \'name\' - Fetches a role from apm\n
  submit - Publishes current role/playbook to apm''')

def main():
  config = os.path.expanduser('~/.apm')  # if file doesn't exit, create it.
  parser = ConfigParser.ConfigParser()

  if len(sys.argv) < 2:
    printMenu()

  option = sys.argv[1]

  if option == 'init':
    init()
  elif option == 'generate':
    generate(sys.argv[2])
  elif option == 'get':
    if len(sys.argv) >= 3:
      get()
    else:
      printMenu()
  elif option == 'submit':
    submit(config, parser)
  else:
    printMenu()



if __name__ == '__main__':
  main()