from modules.logger import Logger

class MonthToIntegerConverter(object):
    def __init__(self):
        self.logger = Logger()
        self.months = [
            'NoneToMakeNumberNotStupid',
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
        ]

    def get_month(self, month):
        try:
            return self.months.index(month)
        except Exception as e:
            self.logger.error('Error converting month string to integer value: {}'.format(e))