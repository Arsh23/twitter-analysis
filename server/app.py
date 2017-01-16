import os
import json

from flask import Flask, render_template, jsonify


app = Flask(__name__)
app.secret_key = 's0mth1ng s3cr3t'


@app.route('/freq')
def freq():
    return render_template('freqgraph.html')


@app.route('/top10')
def top10():
    return render_template('top10graph.html')


@app.route('/sentiment')
def sentiment():
    return render_template('sentigraph.html')


@app.route('/get/<file>')
def get(file):
    if file in ['freq', 'top10', 'sentiment']:
        with open('static/data/'+file+'.json') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return 'File not Found !'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
