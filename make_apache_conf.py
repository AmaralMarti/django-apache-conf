# -*- coding: utf-8 -*-
import os, sys

def get_url():
	if len(sys.argv) != 2:
		raise Exception('URL não informada')
	
	return sys.argv[1]

def get_project_name():
	current_path = os.path.dirname(os.path.abspath(__name__))
	current_path = current_path.split('/')

	return current_path[len(current_path) - 1]

def get_project_path(project_name):
	project_home = os.environ['PROJECT_HOME']	

	return os.path.join(project_home, project_name)

def get_environment_path(project_name):
	workon_home = os.environ['WORKON_HOME']	

	return os.path.join(workon_home, project_name)

def get_wsgi_path():
	result = ''
	for item in os.listdir('.'):
		if os.path.isdir(item):
			os.chdir(item)
			if os.path.exists('wsgi.py'):
				result = item
				os.chdir('..')
				break
			else:
				os.chdir('..')

	return result

def create_file(url, project_name, project_path, environment_path):
	file_name = project_name + '.conf'
	if os.path.exists(file_name):
		os.remove(file_name)

	wsgi_path = get_wsgi_path()

	file = open(file_name, 'w')
	
	file.write('WSGIDaemonProcess {} python-path={}:{}/lib/python2.7/site-packages\n'.format(url, project_path, environment_path))
	file.write('WSGIProcessGroup {}\n\n'.format(url))

	file.write('<VirtualHost *:80>\n')
	file.write('\tServerName {}\n'.format(url))
	file.write('\tWSGIScriptAlias / {}/{}/wsgi.py\n\n'.format(project_path, wsgi_path))

	file.write('\t<Directory {}>\n'.format(project_path))
	file.write('\t\t<Files wsgi.py>\n')
	file.write('\t\t\tRequire all granted\n')
	file.write('\t\t\tOrder allow,deny\n')
	file.write('\t\t\tAllow from all\n')
	file.write('\t\t</Files>\n')
	file.write('\t</Directory>\n\n')

	file.write('\tAlias /media/ {}/media/\n'.format(project_path))
	file.write('\tAlias /static/ {}/static/\n\n'.format(project_path))

	file.write('\t<Directory {}/media>\n'.format(project_path))
	file.write('\t\tRequire all granted\n')
	file.write('\t\tOrder allow,deny\n')
	file.write('\t\tAllow from all\n')
	file.write('\t</Directory>\n\n')

	file.write('\t<Directory {}/static>\n'.format(project_path))
	file.write('\t\tRequire all granted\n')
	file.write('\t\tOrder allow,deny\n')
	file.write('\t\tAllow from all\n')
	file.write('\t</Directory>\n\n')
	file.write('</VirtualHost>')
	file.close()

if  __name__ =='__main__':
	try:
		url = get_url()
		project_name = get_project_name()
		project_path = get_project_path(project_name)
		environment_path = get_environment_path(project_name)
		create_file(url, project_name, project_path, environment_path)
	except Exception as E:
		print E.message
