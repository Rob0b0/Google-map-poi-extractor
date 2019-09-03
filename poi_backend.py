"""
Google POI Scraper Backend
Created in September, 2019
@author: Yunbo Chen
"""
from flask import Flask, request, jsonify, render_template
from helper import CoordBound
import pymongo
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
uri = 'mongodb://root:' + 'Ctdna190a_10000'+ \
    '@dds-2ze8a51ba3f411041814-pub.mongodb.rds.aliyuncs.com:3717,'+\
        'dds-2ze8a51ba3f411042881-pub.mongodb.rds.aliyuncs.com:371'+\
            '7/admin?replicaSet=mgset-10638507'
client = pymongo.MongoClient(uri)
db = client.poi_google2019
# city name
city_name = 'DC'
# dict for reference
type_ref = {'cafe': 'catering', 'bakery': 'catering', 'restaurant':'catering',
    'meal_delivery': 'catering', 'meal_takeaway':'catering',
    'art_gallery': 'culture', 'library': 'culture',
    'museum': 'culture', 'school': 'education',
    'pharmacy': 'hospital', 'hospital': 'hospital',
    'dentist': 'hospital', 'doctor': 'hospital',
    'physiotherapist': 'hospital', 'bar': 'recreation',
    'movie_rental': 'recreation', 'movie_theater': 'recreation',
    'beauty_salon': 'recreation', 'hair_care': 'recreation',
    'laundry': 'recreation', 'spa': "recreation", 'night_club': 'recreation',
    'casino': 'recreation', 'book_store': 'retail', 'convenience_store': 'retail',
    'clothing_store': 'retail', 'department_store': 'retail',
    'shopping_mall': 'retail', 'shoe_store': 'retail',
    'bicycle_store': 'retail', 'electronics_store': 'retail',
    'furniture_store': 'retail', 'hardware_store': 'retail',
    'home_goods_store': 'retail', 'jewelry_store': 'retail',
    'liquor_store': 'retail', 'pet_store': 'retail', 'store': 'retail',
    'supermarket': 'retail', 'gym': 'sport', 'stadium': 'sport',
    'bowling_alley': 'sport', 'airport': 'transport',
    'bus_station': 'transport',
    'parking': 'transport',
    'subway_station': 'transport',
    'taxi_stand': 'transport',
    'train_station': 'transport',
    'transit_station': 'transport'
    }

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/localize/', methods=["POST"])
def main_interface():
    data = request.get_json()['data']
    search_type = request.get_json()['search_type']
    print(len(data))
    # db connection
    for row in data:
        # add unique _id
        row['_id'] = row['id']
        # pop original place id
        row.pop('id', None)
        # form table name
        table_name = "{}_{}".format(city_name, type_ref[search_type])
        try:
            db[table_name].insert_one(row)
        except DuplicateKeyError:
            continue
        except Exception as e:
            print("Unhandled error for row {}\nexception:{}".format(row, e))
            continue
    return "yep"

@app.route('/gridify/', methods=["POST"])
def gridify():
    res = request.get_json()
    coords = CoordBound(res[0]['lat'],
        res[0]['lng'], res[1]['lat'], res[1]['lng'])
    grid_size = coords.get_size()
    grids = coords.one_to_four()
    return jsonify([i.serialize() for i in coords.dividify()])


if __name__ == '__main__':
    app.run(debug=True)