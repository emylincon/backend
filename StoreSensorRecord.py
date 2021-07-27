import datetime as dt
import random
from calendar import monthrange


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

        def random_data(a, b):
            return round(random.uniform(a, b), 2)

        for i in range(1, days + 1):
            my_date = dt.datetime(today.year, today.month, i)

            self.record.temp.add(min_=random_data(10, 15), max_=random_data(20, 35),
                                 avg=random_data(15, 20), today=my_date)

            self.record.hum.add(min_=random_data(10, 15), max_=random_data(20, 35),
                                avg=random_data(15, 20), today=my_date)

            self.record.heat_index.add(min_=random_data(10, 15), max_=random_data(20, 35),
                                       avg=random_data(15, 20), today=my_date)

    def sort_temp(self, reverse: bool = False, kind: str = 'max') -> dict:
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

    def sort_hum(self, reverse: bool = False, kind: str = 'max') -> dict:
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

    def sort_heat_index(self, reverse: bool = False, kind: str = 'max') -> dict:
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
