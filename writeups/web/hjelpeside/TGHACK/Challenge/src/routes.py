from webapp import app
from flask import render_template, url_for, redirect, request, abort
import base64
import binascii
import re
import os
from lxml import etree

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base64', methods=['GET', 'POST'])
def base64_side():
    if request.method == 'POST' and request.form.get('base64'):
        try:
            if request.form.get('action') == 'Kode':
                result = base64.b64encode(request.form.get('base64').encode()).decode()
                return render_template('base64.html', result=result)
            elif request.form.get('action') == 'Dekode':
                result = base64.b64decode(request.form.get('base64')).decode()
                return render_template('base64.html', result=result)
        except:
            return render_template('base64.html', result="Ugyldig input!")
    return render_template('base64.html')

@app.route('/hex', methods=['GET', 'POST'])
def hex_side():
    if request.method == 'POST' and request.form.get('hex'):
        try:
            if request.form.get('action') == 'Kode':
                result = request.form.get('hex').encode('utf-8').hex()
                return render_template('hex.html', result=result)
            elif request.form.get('action') == 'Dekode':
                result = bytes.fromhex(request.form.get('hex')).decode()
                return render_template('hex.html', result=result)
        except:
            return render_template('hex.html', result="Ugyldig input!")
    return render_template('hex.html')


@app.route('/xml', methods=['GET', 'POST'])
def xml_side():
    if request.method == 'POST' and request.form.get('xml'):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.fromstring(request.form.get('xml'), parser)
            dom = etree.tostring(tree.getroottree(), pretty_print=True).decode('utf-8')
            return render_template('xml.html', result=dom)
        except Exception as e:
            dom = str(e)
            return render_template('xml.html', result=dom)
    return render_template('xml.html')

@app.route('/ping', methods=['GET', 'POST'])
def ping_side():
    if request.method == 'POST' and request.form.get('host'):
        try:
            if request.form.get('action') == 'ping':
                if re.match(r'^127\.\d+\.\d+\.\d+$', request.form.get('host')):
                    result = os.popen(f'ping -c 4 {request.form.get("host")}').read()
                    return render_template('ping.html', result=result)
                else:
                    return render_template("ping.html", result="Vi støtter bare localhost enn så lenge!")
        except:
            return render_template('ping.html', result="Ugyldig input!")
    return render_template('ping.html')