from odoo import http
from odoo.http import request
from datetime import datetime,timedelta
from odoo.osv import expression
import ast
import logging
_logger = logging.getLogger(__name__)

class DynamicDashboard(http.Controller):
    """Class to search and filter values in dashboard"""

    @http.route('/tile/details', type='json', auth='user')
    def tile_details(self, **kw):
        """Function to get tile details"""
        tile_id = request.env['dashboard.block'].sudo().browse(
            int(kw.get('id')))
        if tile_id:
            domain = ast.literal_eval(tile_id.filter) if tile_id.filter else []

            if tile_id.time_period:
                today = datetime.today()
                if tile_id.time_period == 'today':
                    start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_of_today = today.replace(hour=23, minute=59, second=59, microsecond=999999)

                    domain.append(('create_date', '>=', start_of_today))
                    domain.append(('create_date', '<=', end_of_today))

                elif tile_id.time_period == 'week':
                    start_of_week = today - timedelta(days=today.weekday())
                    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59,
                                                            microseconds=999999)

                    domain.append(('create_date', '>=', start_of_week))
                    domain.append(('create_date', '<=', end_of_week))

                elif tile_id.time_period == 'month':
                    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    next_month = today.replace(day=28) + timedelta(days=4)  # Ensures we move to next month
                    end_of_month = next_month.replace(day=1, hour=23, minute=59, second=59,
                                                      microsecond=999999) - timedelta(days=1)

                    domain.append(('create_date', '>=', start_of_month))
                    domain.append(('create_date', '<=', end_of_month))

                elif tile_id.time_period == 'year':
                    start_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                    end_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

                    domain.append(('create_date', '>=', start_of_year))
                    domain.append(('create_date', '<=', end_of_year))

            _logger.info(f'============={domain}=====================')
            return {'model': tile_id.model_id.model, 'filter': str(domain),
                    'model_name': tile_id.model_id.name}
        return False

    @http.route('/custom_dashboard/search_input_chart', type='json',
                auth="public", website=True)
    def dashboard_search_input_chart(self, search_input):
        """Function to filter search input in dashboard"""
        return request.env['dashboard.block'].search([
            ('name', 'ilike', search_input)]).ids

