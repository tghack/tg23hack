from flask import Flask, redirect, request, url_for
from random import choice

app = Flask(__name__)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    urls = ["https://www.youtube.com/watch?v=OtlXDNdOgGM", "https://www.youtube.com/watch?v=nqZ_Cb2slBw", "https://www.youtube.com/watch?v=GsJ3plHXVsc"]
    return redirect(choice(urls), code=302) 

@app.route('/qUaK')
def qUaK():
    if request.headers.get('User-Agent') == 'QuakQuak':
        return '<p>Down the rabbit hole we go!</p>'
    return redirect(url_for('catch_all'))

@app.route('/staged')
def staged():
    if request.headers.get('User-Agent') == 'flagplz':
        return '<p>TG23{why all the debug checks?!}'
    return redirect(url_for('catch_all'))

app.run(debug=False, host='0.0.0.0', port=8080)