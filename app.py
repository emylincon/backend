from flask import Flask, jsonify, render_template
import random
import pandas as pd
import datetime as dt
from calendar import monthrange

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


class Pod:
    def __init__(self):
        self.max = {}
        self.min = {}
        self.avg = {}

    @property
    def number_of_days_in_month(self):
        today = dt.datetime.now()
        return monthrange(today.year, today.month)[1]

    def add(self, max_: float, min_: float, avg: float, today=None) -> None:
        """

        :param max_: float max
        :param min_: float min
        :param avg: float avg
        :param today:
        :return: None
        """
        if today is None:
            today_ = dt.datetime.now()
            today = dt.datetime(today_.year, today_.month, today_.day)
        self.max[str(today)] = max_
        self.min[str(today)] = min_
        self.avg[str(today)] = avg


class Days:
    def __init__(self):
        self.temp = Pod()
        self.hum = Pod()
        self.heat_index = Pod()
        self.date = dt.datetime.now()


class MonthDetails:  # MONTH_RECORD
    def __init__(self):
        self.record = Days()
        self.date = dt.datetime.now()

    def coldest(self):
        """
        :return: dict coldest day {date: temp}
        """
        data = self.record.temp.min
        if len(data) == 0:
            return {'response': 'Record is empty'}
        date = min(data, key=data.get)
        min_data = data[date]
        return {date: min_data}

    def hottest(self):
        """
        :return: dict hottest day {date: temp}
        """
        data = self.record.temp.max
        if len(data) == 0:
            return {'response': 'Record is empty'}
        date = max(data, key=data.get)
        max_data = data[date]
        return {date: max_data}

    @staticmethod
    def get_date():
        """
        :return: datetime string
        """
        tod = dt.datetime.now()
        return str(dt.datetime(tod.year, tod.month, tod.day))

    def update(self, describe):
        """
        updates the record temp, hum and heat index
        describe
                temperature   humidity  heat_index
        count     2.000000   2.000000    2.000000
        mean     15.268681  27.901305   19.956433
        std       7.451040  11.174133    7.009454
        min      10.000000  20.000000   15.000000
        25%      12.634341  23.950653   17.478216
        50%      15.268681  27.901305   19.956433
        75%      17.903022  31.851958   22.434649
        max      20.537362  35.802610   24.912865
        """
        if self.date.month < dt.datetime.now().month:
            self.record = Days()
            self.date = dt.datetime.now()

        self.record.temp.add(min_=describe['temperature']['min'], max_=describe['temperature']['max'],
                             avg=describe['temperature']['mean'])

        self.record.hum.add(min_=describe['humidity']['min'], max_=describe['humidity']['max'],
                            avg=describe['humidity']['mean'])

        self.record.heat_index.add(min_=describe['heat_index']['min'], max_=describe['heat_index']['max'],
                                   avg=describe['heat_index']['mean'])

    def test_data(self):
        """
        populates all the days of the current month in the record with random data for testing purposes
        :returns None
        """
        today = dt.datetime.now()
        days = monthrange(today.year, today.month)[1]

        def random_data(a,b):
            return round(random.uniform(a, b), 2)

        for i in range(1, days + 1):
            my_date = dt.datetime(today.year, today.month, i)

            self.record.temp.add(min_=random_data(10,15), max_=random_data(20,35),
                                 avg=random_data(15,20), today=my_date)

            self.record.hum.add(min_=random_data(10,15), max_=random_data(20,35),
                                 avg=random_data(15,20), today=my_date)

            self.record.heat_index.add(min_=random_data(10,15), max_=random_data(20,35),
                                 avg=random_data(15,20), today=my_date)

    def sort_temp(self, reverse: bool = False, kind : str = 'max') -> dict:
        """
        Sorts the temperature record
        :param reverse: Boolean variable, determines if sorting is reversed
        :param kind: sting variable can be max, min or avg
        :return: sorted dictionary
        """
        if kind == 'max':
            return dict(sorted(self.record.temp.max.items(), key=lambda item: item[1], reverse=reverse))
        elif kind == 'avg':
            return dict(sorted(self.record.temp.avg.items(), key=lambda item: item[1], reverse=reverse))
        else:
            return dict(sorted(self.record.temp.min.items(), key=lambda item: item[1], reverse=reverse))

    def sort_hum(self, reverse: bool = False, kind : str = 'max') -> dict:
        """
        Sorts the humidity record
        :param reverse: Boolean variable, determines if sorting is reversed
        :param kind: sting variable can be max, min or avg
        :return: sorted dictionary
        """
        if kind == 'max':
            return dict(sorted(self.record.hum.max.items(), key=lambda item: item[1], reverse=reverse))
        elif kind == 'avg':
            return dict(sorted(self.record.hum.avg.items(), key=lambda item: item[1], reverse=reverse))
        else:
            return dict(sorted(self.record.hum.min.items(), key=lambda item: item[1], reverse=reverse))

    def sort_heat_index(self, reverse: bool = False, kind : str = 'max') -> dict:
        """
        Sorts the heat index record
        :param reverse: Boolean variable, determines if sorting is reversed
        :param kind: sting variable can be max, min or avg
        :return: sorted dictionary
        """
        if kind == 'max':
            return dict(sorted(self.record.heat_index.max.items(), key=lambda item: item[1], reverse=reverse))
        elif kind == 'avg':
            return dict(sorted(self.record.heat_index.avg.items(), key=lambda item: item[1], reverse=reverse))
        else:
            return dict(sorted(self.record.heat_index.min.items(), key=lambda item: item[1], reverse=reverse))


MONTH_RECORD = MonthDetails()


class GenData:  # DATA_OBJ
    def __init__(self) -> None:
        self.data = pd.DataFrame({'temperature': [random.uniform(1, 35)], 'humidity': [random.uniform(25, 70)],
                                  'heat_index': [random.uniform(1, 35)]})
        self.date = dt.datetime.now()
        self.size_limit = 1000

    def add(self) -> None:
        """
        adds randomly generated values to record
        :return: None
        """
        temp: float = random.uniform(1, 35)
        hum: float = random.uniform(25, 70)
        print(self.size_limit)
        if len(self.data) >= self.size_limit:   # if length of store is equal or greater than the limit remove first row
            self.data = self.data.iloc[1:, :]
        self.data.loc[self.data.index[-1]+1] = [temp, hum, self.calculate_heat_index(temp, hum)]

    @staticmethod
    def calculate_heat_index(temperature: float, humidity: float) -> float:
        """
        formula has been obtained from https://en.wikipedia.org/wiki/Heat_index
        :param temperature:
        :param humidity:
        :return: heat index
        """
        constant = {'c1': -8.78469475556,
                    'c2': 1.61139411,
                    'c3': 2.33854883889,
                    'c4': -0.14611605,
                    'c5': -0.012308094,
                    'c6': -0.0164248277778,
                    'c7': 0.002211732,
                    'c8': 0.00072546,
                    'c9': -0.000003582}

        funcs = lambda t, h: constant['c1'] + (constant['c2'] * t) + (constant['c3'] * h) + (constant['c4'] * h * t) + (
                constant['c5'] * t ** 2) + (constant['c6'] * h ** 2) + (constant['c7'] * t ** 2 * h) + (
                                     constant['c8'] * t * h ** 2) + (constant['c9'] * (t ** 2) * (h ** 2))

        return funcs(temperature, humidity)

    def update_month(self):
        """
        updates the months daily record if new day
        :return: None
        """
        today = dt.datetime.now()
        if self.date.day < today.day:
            data = self.data.describe()
            describe = {'temperature': data.temperature.to_dict(), 'humidity': data.humidity.to_dict(), 'heat_index':
                data.heat_index.to_dict()}
            MONTH_RECORD.update(describe=describe)

    def get_data(self):
        """
        adds data, update month record and return record describe
        :return: DataFrame
        """
        self.add()
        self.update_month()
        return self.data.describe()


DATA_OBJ = GenData()
display_data1 = {'actual': {'sensor': {'heat_index': 24.94215049377219, 'temperature': 21.0, 'humidity': 51.0,
                                       'datetime': '29-09-2020 10:22:37', 'id': 3018},
                            'lstm': {'heat_index': 26.94215049377219, 'temperature': 18.350318908691406,
                                     'humidity': 38.90366744995117, 'datetime': '29-09-2020 10:22:37', 'id': 3018},
                            'arima': {'heat_index': 25.763476888337447, 'temperature': 25.0,
                                      'humidity': 43.40027524883986, 'datetime': '29-09-2020 10:22:37', 'id': 3018}},
                 'data_stat': {'temperature': {'count': {'data': 3018.0, 'arrow': 'up', '%': 0.57},
                                               'mean': {'data': 25.12, 'arrow': 'down', '%': 0.09},
                                               'std': {'data': 0.50, 'arrow': 'up', '%': 27.04},
                                               'min': {'data': 20.26, 'arrow': 'equal', '%': 0.0},
                                               'max': {'data': 26.0, 'arrow': 'equal', '%': 0.0}},
                               'humidity': {'count': {'data': 3018.0, 'arrow': 'up', '%': 0.57},
                                            'mean': {'data': 39.13, 'arrow': 'up', '%': 0.18},
                                            'std': {'data': 1.48, 'arrow': 'up', '%': 31.31},
                                            'min': {'data': 36.0, 'arrow': 'equal', '%': 0.0},
                                            'max': {'data': 53.0, 'arrow': 'up', '%': 26.19}},
                               'heat_index': {'count': {'data': 3018.0, 'arrow': 'up', '%': 0.57},
                                              'mean': {'data': 25.74, 'arrow': 'down', '%': 0.02},
                                              'std': {'data': 0.24, 'arrow': 'up', '%': 3.42},
                                              'min': {'data': 20.55, 'arrow': 'equal', '%': 0.0},
                                              'max': {'data': 26.27, 'arrow': 'equal', '%': 0.0}}},
                 'pred_stat': {'lstm': {
                     'hum': {'rmse': 2.35, 'date': '21-10-2020 16:58:53', 'accuracy': 82.62, 'arrow': 'up',
                             'loss': 17.38},
                     'temp': {'rmse': 0.88, 'date': '21-10-2020 16:54:57', 'accuracy': 79.43, 'arrow': 'up',
                              'loss': 20.57},
                     'heat': {'rmse': 0.35, 'date': '21-10-2020 16:56:46', 'accuracy': 87.84, 'arrow': 'up',
                              'loss': 12.16}},
                     'arima': {'hum': {'rmse': 1.11, 'date': '24-09-2020 19:09:36', 'arrow': 'up'},
                               'temp': {'rmse': 0.90, 'date': '24-09-2020 19:09:36', 'arrow': 'down'},
                               'heat': {'rmse': 1.24, 'date': '24-09-2020 19:09:36', 'arrow': 'up'}}}}


class DataStat:
    """:key
    {'temperature': {'count': 3001.0, 'mean': 25.1823592136, 'std': 0.39777284, 'min': 20.26, '25%': 25.0, '50%': 25.0, '75%': 25.0, 'max': 26.0},
    'id': {'count': 3001.0, 'mean': 1501.0, 'std': 866.4584044642, 'min': 1.0, '25%': 751.0, '50%': 1501.0, '75%': 2251.0, 'max': 3001.0},
    'humidity': {'count': 3001.0, 'mean': 39.0640153282, 'std': 1.1322446902, 'min': 36.0, '25%': 38.0, '50%': 39.0, '75%': 40.0, 'max': 42.0},
    'heat_index': {'count': 3001.0, 'mean': 25.7518516255, 'std': 0.2332050521, 'min': 20.55, '25%': 25.6297423111, '50%': 25.6834783556, '75%': 25.6834783556, 'max': 26.2747953298}}
    """

    def __init__(self):
        self.stat = DATA_OBJ.data.describe().fillna(0)
        self.units = ['temperature', 'humidity', 'heat_index']
        self.metrics = ['count', 'mean', 'std', 'min', 'max']

    @staticmethod
    def percentage(new_value, old_value):
        """

        :param new_value:
        :param old_value:
        :return: float
        """
        if old_value == 0:
            return 0
        return round((abs(new_value - old_value) / old_value) * 100, 2)

    @staticmethod
    def get_arrow(new_value, old_value):
        """

        :param new_value:
        :param old_value:
        :return: str
        """
        arrow = 'down'
        if new_value > old_value:
            arrow = 'up'
        elif new_value == old_value:
            arrow = 'equal'
        return arrow

    def get_stat(self, pred_stat=0):
        """
        returns data to display
        :param pred_stat: 0 or 1
        :return: dict
        """
        new_stat = DATA_OBJ.get_data().fillna(0)
        # new_stat[i]
        res = {i: {j: {'data': round(new_stat[i][j], 2), 'arrow': self.get_arrow(new_stat[i][j], self.stat[i][j]),
                       '%': self.percentage(new_stat[i][j], self.stat[i][j])} for j in self.metrics} for i in
               self.units}
        display = {'actual': {'sensor': DATA_OBJ.data.loc[DATA_OBJ.data.index[-1]].to_dict()}, 'data_stat': res}
        if pred_stat == 1:
            for key in ['lstm', 'arima']:
                display['actual'][key] = {}
            for key in ['lstm', 'arima']:
                for k, v in display['actual']['sensor'].items():
                    diff = random.uniform(1, 3)
                    display['actual'][key][k] = v - diff
        self.stat = new_stat
        return display

    @staticmethod
    def pred_stat():
        """

        :return: dict
        """
        date = str(dt.datetime.now()).split('.')[0]

        def arrow():
            arr = ['up', 'down']
            return random.choice(arr)

        def loss():
            acc = {'loss': round(random.uniform(1, 30), 2)}
            acc['accuracy'] = 100 - acc['loss']
            return acc

        return {'lstm': {
            'hum': {'rmse': round(random.uniform(1, 4), 2), 'date': date, 'arrow': arrow(), **loss()},
            'temp': {'rmse': round(random.uniform(1, 4), 2), 'date': date, 'arrow': arrow(), **loss()},
            'heat': {'rmse': round(random.uniform(1, 4), 2), 'date': date, 'arrow': arrow(), **loss()}
        },
            'arima': {'hum': {'rmse': round(random.uniform(1, 4), 2), 'date': date, 'arrow': arrow()},
                      'temp': {'rmse': round(random.uniform(1, 4), 2), 'date': date, 'arrow': arrow()},
                      'heat': {'rmse': round(random.uniform(1, 4), 2), 'date': date, 'arrow': arrow()}}}

    def all_stat(self):
        """

        :return: dict for both get stat and pred stat
        """
        return {**self.get_stat(pred_stat=1), 'pred_stat': self.pred_stat()}


STAT_OBJ = DataStat()


# display_data = {'actual': {'sensor': {'heat_index': 24.94215049377219, 'temperature': 21.0, 'humidity': 51.0,
#                                       'datetime': '29-09-2020 10:22:37', 'id': 3018},
#                            },
#                 'data_stat': {'temperature': {'count': {'data': 3018.0, 'arrow': 'up', '%': 0.57},
#                                               'mean': {'data': 25.12, 'arrow': 'down', '%': 0.09},
#                                               'std': {'data': 0.50, 'arrow': 'up', '%': 27.04},
#                                               'min': {'data': 20.26, 'arrow': 'equal', '%': 0.0},
#                                               'max': {'data': 26.0, 'arrow': 'equal', '%': 0.0}},
#                               'humidity': {'count': {'data': 3018.0, 'arrow': 'up', '%': 0.57},
#                                            'mean': {'data': 39.13, 'arrow': 'up', '%': 0.18},
#                                            'std': {'data': 1.48, 'arrow': 'up', '%': 31.31},
#                                            'min': {'data': 36.0, 'arrow': 'equal', '%': 0.0},
#                                            'max': {'data': 53.0, 'arrow': 'up', '%': 26.19}},
#                               'heat_index': {'count': {'data': 3018.0, 'arrow': 'up', '%': 0.57},
#                                              'mean': {'data': 25.74, 'arrow': 'down', '%': 0.02},
#                                              'std': {'data': 0.24, 'arrow': 'up', '%': 3.42},
#                                              'min': {'data': 20.55, 'arrow': 'equal', '%': 0.0},
#                                              'max': {'data': 26.27, 'arrow': 'equal', '%': 0.0}}},

#                 }

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
    # MONTH_RECORD.test_data() # This populates record with random data for test
    app.run(port=5555)
