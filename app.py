from flask import Flask, jsonify, request, render_template
import re
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


app = Flask(__name__)


@app.route('/')
def index():
    ip = os.environ['HOST_IP']
    return render_template('index.html', ip = ip)


@app.route('/search', methods=['POST', 'GET'])
def hello():
    search_term = request.args.get('term')
    results = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&utf8=1&srsearch='+search_term)
    results = results.json()
    response = []
    for key in results:
        if key == 'query':
            query_results = results[key]
            for k1 in query_results:
                if k1 == 'search':
                    search_raw = query_results[k1]
                    for k2 in search_raw:
                        for k, v in k2.items():
                            if k == 'snippet':
                                response.append(v)
    clean_output = []
    for each in response:
        output = cleanhtml(each)
        clean_output.append(output)
    return (render_template('results.html', results=clean_output))


if __name__ == "__main__":
    app.run(debug=True)
