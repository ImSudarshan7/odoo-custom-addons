# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2019-Present Lekhnath Rijal <mail@lekhnathrijal.com.np>
#
##########################################################################

from odoo import fields
from datetime import datetime, date
from time import mktime
import math
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

class ConvertDate(object):
    AD_DATE_START = fields.Date.from_string('1933-04-12')
    BS_DATE_START = (1990, 1, 1)
    DATA = {
        "1990" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "1991" : [31,32,31,32,31,30,30,29,30,29,30,30],
        "1992" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "1993" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "1994" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "1995" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "1996" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "1997" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "1998" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "1999" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2000" : [30,32,31,32,31,30,30,30,29,30,29,31],
        "2001" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2002" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2003" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2004" : [30,32,31,32,31,30,30,30,29,30,29,31],
        "2005" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2006" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2007" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2008" : [31,31,31,32,31,31,29,30,30,29,29,31],
        "2009" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2010" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2011" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2012" : [31,31,31,32,31,31,29,30,30,29,30,30],
        "2013" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2014" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2015" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2016" : [31,31,31,32,31,31,29,30,30,29,30,30],
        "2017" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2018" : [31,32,31,32,31,30,30,29,30,29,30,30],
        "2019" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "2020" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2021" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2022" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "2023" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "2024" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2025" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2026" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2027" : [30,32,31,32,31,30,30,30,29,30,29,31],
        "2028" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2029" : [31,31,32,31,32,30,30,29,30,29,30,30],
        "2030" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2031" : [30,32,31,32,31,30,30,30,29,30,29,31],
        "2032" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2033" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2034" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2035" : [30,32,31,32,31,31,29,30,30,29,29,31],
        "2036" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2037" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2038" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2039" : [31,31,31,32,31,31,29,30,30,29,30,30],
        "2040" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2041" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2042" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2043" : [31,31,31,32,31,31,29,30,30,29,30,30],
        "2044" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2045" : [31,32,31,32,31,30,30,29,30,29,30,30],
        "2046" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2047" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2048" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2049" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "2050" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "2051" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2052" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2053" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "2054" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "2055" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2056" : [31,31,32,31,32,30,30,29,30,29,30,30],
        "2057" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2058" : [30,32,31,32,31,30,30,30,29,30,29,31],
        "2059" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2060" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2061" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2062" : [30,32,31,32,31,31,29,30,29,30,29,31],
        "2063" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2064" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2065" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2066" : [31,31,31,32,31,31,29,30,30,29,29,31],
        "2067" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2068" : [31,31,32,32,31,30,30,29,30,29,30,30],
        "2069" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2070" : [31,31,31,32,31,31,29,30,30,29,30,30],
        "2071" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2072" : [31,32,31,32,31,30,30,29,30,29,30,30],
        "2073" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2074" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2075" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2076" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "2077" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "2078" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2079" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2080" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "2081" : [31,31,32,32,31,30,30,30,29,30,30,30],
        "2082" : [30,32,31,32,31,30,30,30,29,30,30,30],
        "2083" : [31,31,32,31,31,30,30,30,29,30,30,30],
        "2084" : [31,31,32,31,31,30,30,30,29,30,30,30],
        "2085" : [31,32,31,32,30,31,30,30,29,30,30,30],
        "2086" : [30,32,31,32,31,30,30,30,29,30,30,30],
        "2087" : [31,31,32,31,31,31,30,30,29,30,30,30],
        "2088" : [30,31,32,32,30,31,30,30,29,30,30,30],
        "2089" : [30,32,31,32,31,30,30,30,29,30,30,30],
        "2090" : [30,32,31,32,31,30,30,30,29,30,30,30],
        "2091" : [31,31,32,31,31,31,30,30,29,30,30,30],
        "2092" : [30,31,32,32,31,30,30,30,29,30,30,30],
        "2093" : [30,32,31,32,31,30,30,30,29,30,30,30],
        "2094" : [31,31,32,31,31,30,30,30,29,30,30,30],
        "2095" : [31,31,32,31,31,31,30,29,30,30,30,30],
        "2096" : [30,31,32,32,31,30,30,29,30,29,30,30],
        "2097" : [31,32,31,32,31,30,30,30,29,30,30,30],
        "2098" : [31,31,32,31,31,31,29,30,29,30,29,31],
        "2099" : [31,31,32,31,31,31,30,29,29,30,30,30],
        "2100" : [31,32,31,32,31,30,30,30,29,29,30,31],
        "2101" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2102" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2103" : [31,32,31,32,31,30,30,30,29,29,30,30],
        "2104" : [31,32,31,32,31,30,30,30,29,30,29,31],
        "2105" : [31,31,31,32,31,31,30,29,30,29,30,30],
        "2106" : [31,31,32,31,31,31,30,29,30,29,30,30],
        "2107" : [31,32,31,32,31,30,30,30,29,29,30,30],
    }



    @staticmethod
    def ad2bs(ad_date):

        if not isinstance(ad_date, date):
            raise ValueError('Invalid date')

        if isinstance(ad_date, datetime):
            ad_date = ad_date.date()

        if ad_date < ConvertDate.AD_DATE_START:
            raise ValueError("Date out of conversion range")

        days_from_start_date_ad = math.floor(
            (mktime(ad_date.timetuple()) - mktime(ConvertDate.AD_DATE_START.timetuple())) / 86400
        )
        (bs_year, bs_month, bs_date) = ConvertDate.BS_DATE_START[:]

        while days_from_start_date_ad > 0:

            days_in_bs_year = sum(ConvertDate.DATA[str(bs_year)])

            if days_in_bs_year >= days_from_start_date_ad:

                for i in range(12):
                    days_in_bs_month = ConvertDate.DATA[str(bs_year)][i]

                    if days_in_bs_month >= days_from_start_date_ad:
                        bs_date = int(days_from_start_date_ad)
                        days_from_start_date_ad = 0
                        break
                    else:
                        bs_month += 1
                        days_from_start_date_ad -= days_in_bs_month

            else:
                bs_year += 1
                days_from_start_date_ad -= days_in_bs_year

        return (bs_year, bs_month, bs_date)

    @staticmethod
    def bs2ad(from_date):
        days_from_start_date_bs = 0
        (bs_year, bs_month, bs_date) = from_date

        for bs_year_l in range(ConvertDate.BS_DATE_START[0], bs_year):
            days_from_start_date_bs += sum(ConvertDate.DATA[str(bs_year_l)])

        days_from_start_date_bs += sum(
            ConvertDate.DATA[str(bs_year)][:bs_month - 1]
        )

        days_from_start_date_bs +=bs_date

        timestamp = mktime(ConvertDate.AD_DATE_START.timetuple()) + (days_from_start_date_bs * 86400)

        return datetime.fromtimestamp(timestamp).date()


class BikramSamvat(object):
    MONTHS_FULL_EN = ['Baisakh', 'Jestha', 'Aashad', 'Shrawan', 'Bhadra', 'Aaswin','Kartik', 'Mangsir', 'Paush', 'Magh', 'Falgun', 'Chaitra']
    __ad_date = None

    def __init__(self, year=None, month=None, day=None):
        self.__convert__(year or date.today(), month, day)

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day} ({self.date.strftime('%Y-%m-%d')})"

    def __repr__(self):
        return self.__str__()

    def __sub__(self, delta):
        if not isinstance(delta, relativedelta):
            raise ValueError('Cannot subtract "%s" with type "%s"' % (BikramSamvat.__name__, type(delta).__name__))

        if delta.years:
            year = self.year - delta.years
            day = self.day

            days_in_month = ConvertDate.DATA[str(year)][self.month - 1]
            if days_in_month < self.day:
                day = days_in_month

            self.__convert__(year, self.month, day)

        if delta.months:
            delta_years = int(delta.months / 12)
            delta_months = delta.months % 12
            year = self.year - delta_years
            month = self.month - delta_months
            day = self.day

            if month < 1:
                month += 12
                year -= 1

            days_in_month = ConvertDate.DATA[str(year)][month - 1]
            if days_in_month < self.day:
                day = days_in_month

            self.__convert__(year, month, day)

        if delta.days: # NOTE: handles both weeks and days (ie 1 week = 7 days)
            self.date = self.__ad_date - relativedelta(days=delta.days)

        return self

    def __add__(self, delta):
        if not isinstance(delta, relativedelta):
            raise ValueError('Cannot add "%s" with type "%s"' % (BikramSamvat.__name__, type(delta).__name__))

        if delta.years:
            year = self.year + delta.years
            day = self.day

            days_in_month = ConvertDate.DATA[str(year)][self.month - 1]

            if days_in_month < self.day:
                day = days_in_month

            self.__convert__(year, self.month, day)

        if delta.months:
            delta_years = int(delta.months / 12)
            delta_months = delta.months % 12

            year = self.year + delta_years
            month = self.month + delta_months
            day = self.day

            if month > 12:
                month -= 12
                year += 1

            days_in_month = ConvertDate.DATA[str(year)][month - 1]
            if days_in_month < self.day:
                day = days_in_month

            self.__convert__(year, month, day)

        if delta.days: # NOTE: handles both weeks and days (ie 1 week = 7 days)
            self.date = self.__ad_date + relativedelta(days=delta.days)

        return self


    def __convert__(self, year, month=None, day=None):
        ad_date = None

        if isinstance(year, date):
            ad_date = year
            (year, month, day) = ConvertDate.ad2bs(year)

        if not all([year, month, day]):
            raise ValueError("Invalid BikramSamvat")

        if month < 1 or month > 12:
            raise ValueError('Invalid BikramSamvat month')
        elif not ConvertDate.DATA.get(str(year)):
            raise ValueError('Invalid BikramSamvat year')
        elif ConvertDate.DATA[str(year)][month - 1] < day:
            raise ValueError('Invalid BikramSamvat day')

        self.year = year
        self.month = month
        self.day = day

        if ad_date is None:
            ad_date = ConvertDate.bs2ad((year, month, day))

        self.__ad_date = ad_date

    def format(self, date_format):
        return date_format \
            .replace('MM', '{r1}') \
            .replace('mm', '{r2:p}') \
            .replace('m', '{r2}') \
            .replace('dd', '{r3:p}') \
            .replace('d', '{r3}') \
            .replace('yyyy', '{r4}') \
            .replace('yy', '{r5}') \
            .replace('p', '02d') \
            .format(
                #NOTE: Don't include format char ie(M,m,d,y,p) in dict key
                r1 = BikramSamvat.MONTHS_FULL_EN[self.month - 1],
                r2=self.month,
                r3=self.day,
                r4=self.year,
                r5 = abs(self.year % 100),
            )

    @property
    def ymd(self):
        return (self.year, self.month, self.day)

    @property
    def date(self):
        return self.__ad_date

    @date.setter
    def date(self, ad_date):
        if not isinstance(ad_date, date):
            raise ValueError('Invalid date')

        self.__convert__(ad_date)
