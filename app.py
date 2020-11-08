from flask import Flask, jsonify, request, render_template
import re
import requests
import os
import pandas
import random
from dotenv import load_dotenv
load_dotenv()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def process_data(results):
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
    return clean_output


def process_image_urls(results):
    image_response = []
    results = results.json()
    return results
app = Flask(__name__)

def read_csv_and_find_random_id ():
    df = pandas.read_csv('processed_output.csv')
    entire_list = df.to_numpy().flatten()
    return (random.choice(entire_list))

@app.route('/')
def index():
    random_person = read_csv_and_find_random_id()
    ip = os.environ['HOST_IP']
    return render_template('index.html', **locals())


@app.route('/search', methods=['POST', 'GET'])
def hello():
    search_term = request.args.get('term')

    results = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&utf8=1&srsearch='+search_term)
    results = results.json()
    clean_output = process_data(results)
    # image_results = requests.get('https://commons.wikimedia.org/w/api.php?action=query&generator=images&prop=imageinfo&gimlimit=500&redirects=1&titles='+search_term+'&iiprop=timestamp|user|userid|comment|canonicaltitle|url|size|dimensions|sha1|mime|thumbmime|mediatype|bitdepth&format=json')
    # cleaned_image_output = process_image_urls(image_results)
    return (render_template('results.html', results=clean_output))


if __name__ == "__main__":
    app.run(debug=True)
