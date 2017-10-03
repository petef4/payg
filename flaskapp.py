from json import load

from flask import Flask, redirect, render_template, request, send_from_directory

from eff_min import add_effective_per_min
from grader import Grader
from imaging import Imaging, open_here

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

new_host = 'payg.pythonanywhere.com'


@app.after_request
def gnu_terry_pratchett(resp):
    resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp


with open_here('payg.json') as f:
    data = load(f)
if app.config['DO_AVERAGE']:
    add_effective_per_min(data, app.config['MAXIMUM_CALL'])

with open_here('grading.json') as f:
    grading = load(f)
grader = Grader(grading)
grader.grade(data)

img = Imaging()
img.add_logo_pos(data)

counts = {'operator': len(set(r['operator'] for r in data)),
          'plan': len(data)}
if app.config['DO_AVERAGE']:
    cols = ['operator', 'plan', 'min_same', 'min_other', 'min_land',
            'charge_min', 'bill_per', 'eff_min', 'sms_same', 'sms_other',
            'voicemail', '08x', 'mms', '4G', 'tether', 'data', 'network',
            'checked']
else:
    cols = ['operator', 'plan', 'min_same', 'min_other', 'min_land',
            'charge_min', 'bill_per', 'sms_same', 'sms_other', 'voicemail',
            '08x', 'mms', '4G', 'tether', 'data', 'network', 'checked']


def http():
    return (
        request.environ.get('HTTP_X_FORWARDED_PROTO') or  # OpenShift
        request.environ.get('wsgi.url_scheme') or  # PythonAnywhere, localhost
        'http')


@app.route('/')
def payg():
    return redirect('{0}://{1}/'.format(http(), new_host), code=301)


@app.route('/home')
def home():
    return redirect('{0}://{1}/home'.format(http(), new_host), code=301)


@app.route('/links')
def links():
    return redirect('{0}://{1}/links'.format(http(), new_host), code=301)


@app.route('/shopping')
def shopping():
    return redirect('{0}://{1}/shopping'.format(http(), new_host), code=301)


@app.route('/robots.txt')
@app.route('/favicon.ico')
@app.route('/google2427ff77d057f518.html')
@app.route('/BingSiteAuth.xml')
def static_from_root():
    return redirect('{0}://{1}/{2}'.format(http(), new_host, request.path[1:]), code=301)


@app.route('/test')
def test():
    return redirect('{0}://{1}/test'.format(http(), new_host), code=301)


if __name__ == '__main__':
    app.run(debug=True)
