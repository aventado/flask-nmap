#!/usr/bin/env python
import subprocess
from flask import Flask
from flask import render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ADf;laksdjfAdfoiwdkljfaSDF'
manager = Manager(app)
Bootstrap(app)

class Hosts(Form):
	hosts = TextAreaField('Hosts or IP Addresses', validators=[Required()])
	submit = SubmitField('Scan Hosts')

@app.route('/', methods=['GET', 'POST'])
def main():
	ios = {}
	ios_id = 1
	form = Hosts()
	hosts = form.hosts.data
	h = None
	ssh = None
	telnet = None
	if form.validate_on_submit():
		hosts = hosts.split()
		for h in hosts:
			proc = subprocess.Popen(['nmap -p 22,23 %s' % h], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()

			out = out.split('\n')

			for service in out:
				if '22' and 'ssh' in service:
					ssh = service.split()
					ssh = ssh[-2]
				if '23' and 'telnet' in service:
					telnet = service.split()
					telnet = telnet[-2]
		
			ios[ios_id] = {}
			ios[ios_id]['host'] = h
			ios[ios_id]['ssh'] = ssh
			ios[ios_id]['telnet'] = telnet

			ios_id += 1
				
		return render_template('base.html', form=form, ios=ios)

	return render_template('base.html', form=form, ios=ios)

if __name__ == '__main__':
	manager.run()
