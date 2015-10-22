from flask import Flask, render_template, request
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def payg():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template('payg.html', http=http)


@app.route('/home')
def home():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template('home.html', http=http)


@app.route('/links')
def links():
    http = request.environ.get('HTTP_X_FORWARDED_PROTO', 'http')
    return render_template('links.html', http=http)


@app.route('/test')
def test():
    return repr(request.environ)

if __name__ == '__main__':
    app.run(debug=True)
