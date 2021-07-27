import random
import pandas as pd
import datetime as dt


class GenData:  # DATA_OBJ
    def __init__(self, month_record) -> None:
        self.month_record = month_record
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
        if len(self.data) >= self.size_limit:  # if length of store is equal or greater than the limit remove first row
            self.data = self.data.iloc[1:, :]
        self.data.loc[self.data.index[-1] + 1] = [temp, hum, self.calculate_heat_index(temp, hum)]

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
            self.month_record.update(describe=describe)

    def get_data(self):
        """
        adds data, update month record and return record describe
        :return: DataFrame
        """
        self.add()
        self.update_month()
        return self.data.describe()


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


class DataStat:  # STAT_OBJ
    """:key
    {'temperature': {'count': 3001.0, 'mean': 25.1823592136, 'std': 0.39777284, 'min': 20.26, '25%': 25.0, '50%': 25.0, '75%': 25.0, 'max': 26.0},
    'id': {'count': 3001.0, 'mean': 1501.0, 'std': 866.4584044642, 'min': 1.0, '25%': 751.0, '50%': 1501.0, '75%': 2251.0, 'max': 3001.0},
    'humidity': {'count': 3001.0, 'mean': 39.0640153282, 'std': 1.1322446902, 'min': 36.0, '25%': 38.0, '50%': 39.0, '75%': 40.0, 'max': 42.0},
    'heat_index': {'count': 3001.0, 'mean': 25.7518516255, 'std': 0.2332050521, 'min': 20.55, '25%': 25.6297423111, '50%': 25.6834783556, '75%': 25.6834783556, 'max': 26.2747953298}}
    """

    def __init__(self, data_obj):
        self.data_obj = data_obj
        self.stat = self.data_obj.data.describe().fillna(0)
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
        new_stat = self.data_obj.get_data().fillna(0)
        # new_stat[i]
        res = {i: {j: {'data': round(new_stat[i][j], 2), 'arrow': self.get_arrow(new_stat[i][j], self.stat[i][j]),
                       '%': self.percentage(new_stat[i][j], self.stat[i][j])} for j in self.metrics} for i in
               self.units}
        display = {'actual': {'sensor': self.data_obj.data.loc[self.data_obj.data.index[-1]].to_dict()}, 'data_stat': res}
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