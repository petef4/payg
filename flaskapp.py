from json import load

from flask import Flask, render_template, request, send_from_directory

from eff_min import add_effective_per_min
from footnote import definitions
from grader import Grader
from imaging import Imaging, open_here

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.after_request
def gnu_terry_pratchett(resp):
    if request.environ.get('SERVER_NAME') != 'payg.pythonanywhere.com':
        # PythonAnywhere already has this header
        resp.headers.add('X-Clacks-Overhead', 'GNU Terry Pratchett')
    return resp


with open_here('payg.json') as f:
    data = load(f)
active = data['active']
defunct = data['defunct']
footnotes, fn_index = definitions(data['footnotes'])
if app.config['DO_AVERAGE']:
    add_effective_per_min(active, app.config['MAXIMUM_CALL'])

with open_here('grading.json') as f:
    grading = load(f)
grader = Grader(grading)
grader.grade(active)

img = Imaging()
img.add_logo_pos(active)

counts = {'operator': len(set(r['operator'] for r in active)),
          'plan': len(active)}
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
    return render_template(
        'payg.html', http=http(), active=active, cols=cols, grading=grading,
        footnotes=footnotes, fn_index=fn_index, counts=counts,
        do_average=app.config['DO_AVERAGE'])


@app.route('/home')
def home():
    return render_template('home.html', http=http())


@app.route('/links')
def links():
    return render_template('links.html', http=http())


@app.route('/shopping')
def shopping():
    return render_template('shopping.html', http=http())


@app.route('/robots.txt')
@app.route('/favicon.ico')
@app.route('/google2427ff77d057f518.html')
@app.route('/BingSiteAuth.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/test')
def test():
    return render_template('test.html', env=request.environ)


if __name__ == '__main__':
    app.run(debug=True)
