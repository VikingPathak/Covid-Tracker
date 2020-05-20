from flask import Flask, render_template, redirect, url_for, jsonify, request
import requests
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(12)

@app.route("/")
@app.route("/home")
def home():
    return redirect(url_for('covid'))

@app.route("/covid", methods = ["POST", "GET"])
def covid():

    india_data_url = "https://disease.sh/v2/countries/India?yesterday=true&strict=true"
    india_content = requests.get(india_data_url)
    india_data = india_content.json()

    countries_data = countries()
    countries_data_all = country_api()

    return render_template("index.html", data = india_data, countries = countries_data, world = countries_data_all)

@app.route("/countries", methods = ["POST", "GET"])
def countries():

    countries_data_url = "https://coronavirus-tracker-api.herokuapp.com/v2/locations"
    countries_content = requests.get(countries_data_url)
    countries_data = countries_content.json()

    countries_dict = {}
    for item in countries_data['locations']:
        if item['country'] not in countries_dict:
            countries_dict.update({item['country']:{'Population':item['country_population'], 'Confirmed': item['latest']['confirmed'],'Deaths':item['latest']['deaths']}})
        else:
            countries_dict[item['country']]['Confirmed'] += item['latest']['confirmed']
            countries_dict[item['country']]['Deaths'] += item['latest']['deaths']

    return countries_dict

@app.route("/covid/world", methods = ["POST", "GET"])
def world():

    countries_data = countries()
    world_data = country_api()
    return render_template("world.html", countries = countries_data, world = world_data)

@app.route("/covid/india", methods = ["POST", "GET"])
def india():

    from data_render import daywise_data_india
    india_plot_daywise_data = daywise_data_india()
    day = india_plot_daywise_data[0]
    confirmed = india_plot_daywise_data[1]
    deaths = india_plot_daywise_data[2]

    from data_render import statewise_analysis
    statewise_data = statewise_analysis()

    india_data_url = "https://disease.sh/v2/countries/India?yesterday=true&strict=true"
    india_content = requests.get(india_data_url)
    india_data = india_content.json()

    #from data_render import district_zone_analysis
    #states_district_zone_data = district_zone_analysis()
    #district_data = states_district_zone_data

    return render_template("india.html", data = india_data, day = day, confirmed = confirmed, deaths = deaths, states = statewise_data)

@app.route("/covid/contribute")
def contribute():
    return render_template("contribute.html")

@app.route("/daywise_india_data")
def daywise_india_data():

    from data_render import daywise_data_india
    india_plot_daywise_data = daywise_data_india()
    day = india_plot_daywise_data[0]
    confirmed = india_plot_daywise_data[1]
    deaths = india_plot_daywise_data[2]
    
    return jsonify({'day':day, 'confirmed':confirmed, 'deaths':deaths})

def country_api():
    
    world_data = requests.get("https://corona.lmao.ninja/v2/all").json()
    return world_data

if __name__ == "__main__":
    app.run(debug=True)