from json import load

from flask import Flask, render_template, request

from grader import Grader

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

with open('payg.json') as f:
    data = load(f)
with open('grading.json') as f:
    grading = load(f)
grader = Grader(grading)
grader.grade(data)
counts = {'operator': len(set(r['operator'] for r in data)),
          'plan': len(data)}
cols = ['operator', 'plan', 'min_same', 'min_other', 'min_land', 'charge_min',
        'bill_per', 'sms_same', 'sms_other', 'voicemail', '08x', 'mms', 'data',
        'network', 'checked']


@app.route('/')
def payg():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template(
        'payg.html', http=http, data=data, cols=cols, grading=grading,
        counts=counts)


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


@app.route('/test')
def test():
    return render_template('test.html', env=request.environ)

if __name__ == '__main__':
    app.run(debug=True)
