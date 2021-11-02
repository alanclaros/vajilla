"""
Custome db types: date and date time
"""
from django.db import models
from datetime import datetime


class DateTimeFieldCustome(models.DateTimeField):
    """
    Custome Datetime field
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        # print('db_type')
        # typ = ['datetime']
        # See above!
        # if self.null:
        #    typ += ['']
        # if self.precision:
        #    typ += ['default']
        # return ' '.join(typ)

        # sql to create field in database table
        return 'datetime default NULL'

    def to_python(self, value):
        """
        from python to database
        :param value: (datetime) database datetime field
        :return: (str) or None, format: yyyy-mm-dd HH:ii:ss
        """
        #print('to_python')
        # return datetime.from_timestamp(value)
        if value is None:
            return value

        if value == 'now':
            now = datetime.now()
            anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
            mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
            dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
            hora = '0' + str(now.hour) if len(str(now.hour)) == 1 else str(now.hour)
            minutos = '0' + str(now.minute) if len(str(now.minute)) == 1 else str(now.minute)
            segundos = '0' + str(now.second) if len(str(now.second)) == 1 else str(now.second)
            return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minutos + ':' + segundos

        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        # print('get_db_prep_vaule')
        if value is None:
            return None

        if value == 'now':
            now = datetime.now()
            anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
            mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
            dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
            hora = '0' + str(now.hour) if len(str(now.hour)) == 1 else str(now.hour)
            minutos = '0' + str(now.minute) if len(str(now.minute)) == 1 else str(now.minute)
            segundos = '0' + str(now.second) if len(str(now.second)) == 1 else str(now.second)
            return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minutos + ':' + segundos

        return value

    def get_prep_value(self, value):
        # print('get_prep_vaule')
        if value is None:
            return None

        if value == 'now':
            now = datetime.now()
            anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
            mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
            dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
            hora = '0' + str(now.hour) if len(str(now.hour)) == 1 else str(now.hour)
            minutos = '0' + str(now.minute) if len(str(now.minute)) == 1 else str(now.minute)
            segundos = '0' + str(now.second) if len(str(now.second)) == 1 else str(now.second)
            return anio + '-' + mes + '-' + dia + ' ' + hora + ':' + minutos + ':' + segundos

        return value


class DateFieldCustome(models.DateField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        # print('db_type')
        # typ = ['datetime']
        # See above!
        # if self.null:
        #    typ += ['']
        # if self.precision:
        #    typ += ['default']
        # return ' '.join(typ)

        return 'date default NULL'

    def to_python(self, value):
        #print('to_python')
        # return datetime.from_timestamp(value)
        if value is None:
            return value

        if value == 'now':
            now = datetime.now()
            anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
            mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
            dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
            return anio + '-' + mes + '-' + dia

        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        # print('get_db_prep_vaule')
        if value is None:
            return None

        if value == 'now':
            now = datetime.now()
            anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
            mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
            dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
            return anio + '-' + mes + '-' + dia

        return value

    def get_prep_value(self, value):
        # print('get_prep_vaule')
        if value is None:
            return None

        if value == 'now':
            now = datetime.now()
            anio = '20' + str(now.year) if len(str(now.year)) == 2 else str(now.year)
            mes = '0' + str(now.month) if len(str(now.month)) == 1 else str(now.month)
            dia = '0' + str(now.day) if len(str(now.day)) == 1 else str(now.day)
            return anio + '-' + mes + '-' + dia

        return value
