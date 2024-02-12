from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #test

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('formulaire.html') #test

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

from flask import Flask, render_template, jsonify
from datetime import datetime
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Vos routes existantes ici...

@app.route('/commits/')
def commits():
    # Récupérer les données des commits depuis l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()

    # Initialiser un dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}
    for commit in commits:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        if minute not in commits_per_minute:
            commits_per_minute[minute] = 1
        else:
            commits_per_minute[minute] += 1
    
    # Créer les données pour le graphique
    x_values = list(commits_per_minute.keys())
    y_values = list(commits_per_minute.values())
    graph = go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Commits par minute')
    layout = go.Layout(title='Nombre de Commits par Minute', xaxis=dict(title='Minute'), yaxis=dict(title='Nombre de Commits'))
    figure = go.Figure(data=[graph], layout=layout)
    
    return render_template('commits.html', plot=figure.to_html(include_plotlyjs='cdn'))

if __name__ == '__main__':
    app.run(debug=True)



