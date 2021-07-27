from flask import Flask, jsonify, render_template
from GenerateData import GenData, DataStat
from StoreSensorRecord import MonthDetails

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

MONTH_RECORD = MonthDetails()  # Initialize the MonthDetails to store daily and monthly details
# MONTH_RECORD.test_data() # This populates record with random data for test
DATA_OBJ = GenData(month_record=MONTH_RECORD)  # Initialize the GenData to generate data
STAT_OBJ = DataStat(data_obj=DATA_OBJ)  # Initialize the DataStat to format generated data


@app.route('/')
def hello_world():
    """
    :return: html home page
    """
    return render_template('index.html')


@app.route('/get-data')
def get_data():
    """
    endpoint to request data
    :return: json
    """
    return jsonify(STAT_OBJ.get_stat())


@app.route('/set-max-storage/<int:store>')
def set_max_store(store: int):
    """
    sets storage limit
    :param store: int
    :return:  json
    """
    DATA_OBJ.size_limit = store
    print(f'size set {store}')
    return jsonify({'size limit store': store})


@app.route('/hottest-day')
def hottest_day():
    """
    :return: json hottest day
    """
    return jsonify(MONTH_RECORD.hottest())


@app.route('/coldest-day')
def coldest_day():
    """
    :return: json coldest day
    """
    return jsonify(MONTH_RECORD.coldest())


@app.route('/sort_data/<category>/<kind>/<int:reverse>')
def sort_data(category: str, kind: str, reverse: int):
    """
    sorts record data
    :param category: str can be temp, hum or heat index
    :param kind: str can be min, max, avg
    :param reverse: int can be 0 or 1
    :return:
    """
    reverse = True if reverse == 1 else False
    if category == 'temp' or category == 'temperature':
        response = MONTH_RECORD.sort_temp(kind=kind, reverse=reverse)
    elif category == 'hum' or category == 'humidity':
        response = MONTH_RECORD.sort_hum(kind=kind, reverse=reverse)
    else:
        response = MONTH_RECORD.sort_heat_index(kind=kind, reverse=reverse)
    # print(response)
    return jsonify(response)


@app.route('/all-data')
def all_data():
    """
    :return: json
    """
    return jsonify(STAT_OBJ.all_stat())


if __name__ == '__main__':
    app.run(port=5555)
