from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/get_locations', methods = ['GET'])
def get_locations():
    response = jsonify({
        'locations': utils.get_locations()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/estimate_home_price', methods = ['GET', 'POST'])
def estimate_home_price():
    area = float(request.form['area'])
    location = request.form['location']
    rooms = int(request.form['rooms'])
    təmir = request.form['təmir']
    building = request.form['building']

    response = jsonify({
        'estimated_price': utils.estimate_price(location, rooms, area, təmir, building)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    print('Starting server for estimator')
    utils.load_saved_artifacts()
    app.run()