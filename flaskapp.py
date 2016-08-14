from json import load

from flask import Flask, render_template, request, send_from_directory

from eff_min import add_effective_per_min
from grader import Grader

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.after_request
def gnu_terry_pratchett(resp):
    resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
    return resp


with open('payg.json', encoding='UTF-8') as f:
    data = load(f)
if app.config['DO_AVERAGE']:
    add_effective_per_min(data, app.config['MAXIMUM_CALL'])

with open('grading.json', encoding='UTF-8') as f:
    grading = load(f)
grader = Grader(grading)
grader.grade(data)

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


@app.route('/')
def payg():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template(
        'payg.html', http=http, data=data, cols=cols, grading=grading,
        counts=counts, do_average=app.config['DO_AVERAGE'])


@app.route('/home')
def home():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template('home.html', http=http)


@app.route('/links')
def links():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template('links.html', http=http)


@app.route('/shopping')
def shopping():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template('shopping.html', http=http)


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
