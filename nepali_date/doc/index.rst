====================
Nepali Date System
====================

Nepali Date System is a module to convert A.D. to B.S. date and vice versa. This module integrates a nice looking datepicker widget for selecting B.S. dates in each date field. It supports a date selection/conversion range from year 1990 B.S. to year 2107 B.S.


:Authors:
  Lekhnath Rijal <mail@lekhnathrijal.com.np>
:Version: 13.0.6.0
:Last update: August 09, 2021


Server Side Usage
~~~~~~~~~~~~~~~~~~

In server side you can convert any python date instance to a B.S. date using python class ``BikramSamvat`` provided by this module. Following code examples illustrate the usage and available features:

**Instantiate B.S. date**

.. code-block:: python

  # Import date converter
  from odoo.addons.nepali_date.convert_date import BikramSamvat

  # Today's B.S. date
  bs_date_today = BikramSamvat()

  # To get A.D. date from B.S. date instance access `date` property
  ad_date_from_bs_date = bs_date_today.date

**Convert from A.D. date to B.S. date**

.. code-block:: python

  from datetime import date
  import logging

  # Import date converter
  from odoo.addons.nepali_date.convert_date import BikramSamvat

  # Convert from A.D. date
  ad_date = date(1992, 5, 30) # instantiate A.D. date
  ad2bs_date = BikramSamvat(ad_date) # convert from A.D. date to B.S. date

  logging.info(ad2bs_date.format('MM dd, yyyy')) # print formatted B.S. date to stdout
  # Outputs: Jestha 17, 2049


**Convert from B.S. date to A.D. date**

.. code-block:: python

  from datetime import date
  import logging

  # Import date converter
  from odoo.addons.nepali_date.convert_date import BikramSamvat

  # Convert  from B.S. date
  bs_date = BikramSamvat(2046, 12, 12)
  bs2ad_date = bs_date.date # get B.S. to A.D conversion

  logging.info(bs2ad_date.strftime('%B %d, %Y')) # print formatted A.D. date to stdout
  # Outputs: March 25, 1990

  logging.info(bs_date.format('MM dd, yyyy')) # print formatted B.S. date to stdout
  # Outputs: Chaitra 12, 2046

**B.S. date manipulation**

.. code-block:: python

  from datetime import date
  from dateutil.relativedelta import relativedelta

  import logging

  # Import date converter
  from odoo.addons.nepali_date.convert_date import BikramSamvat

  # Instantiate B.S. date
  bs_date = BikramSamvat(2077, 4, 28)

  # Calculate next month based on B.S. date system
  next_month_date_bs = bs_date + relativedelta(months=1)

  # Calculate previous year based on B.S. date system
  prev_year_date_bs = bs_date - relativedelta(years=1)

  # Calculate next week
  next_week_date_bs = bs_date + relativedelta(weeks=1)

  # Complex calculation
  calculated_date_bs = ((BikramSamvat() + relativedelta(years=2, months=6, weeks=2)) - relativedelta(days=1))
  calculated_date_bs_to_ad = calculated_date_bs.date

  # Supported relative properties
  # years, months, weeks and days
