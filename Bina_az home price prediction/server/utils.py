import json
import joblib
import numpy as np

__locations = None
__data_columns = None
__model = None

def estimate_price(location, rooms, area, təmir, building):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = rooms
    if təmir.lower() == 'var':
        x[1] = 1
    else:
        x[1] = 0
    x[2] = area
    if building.lower() == 'yeni':
        x[3] = 1
    else:
        x[3] = 0
    if loc_index >=0:
        x[loc_index] = 1

    return (__model.predict([x])[0]).round(0)

def get_locations():
    return __locations

def get_data_columns():
    return __data_columns

def load_saved_artifacts():
    print('loading saved artifacts...start')
    global __data_columns
    global __locations
    global __model

    with open('server/artifacts/columns.json', 'r') as f:
        __data_columns =  json.load(f)['data_columns']
        __locations = __data_columns[4:]

    with open('server/artifacts/house_price_model.pkl', 'rb') as f:
        __model = joblib.load(f)
    print('loading artifacts...completed')

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_locations())
    import warnings
    warnings.filterwarnings("ignore", message="X does not have valid feature names*")
    print(estimate_price('28 May m.', 3, 125, 'var', 'yeni'))
    print(estimate_price('28 May m.', 3, 120, 'var', 'yeni'))
    print(estimate_price('Elmlər Akademiyası m.', 3, 125, 'var', 'yeni'))