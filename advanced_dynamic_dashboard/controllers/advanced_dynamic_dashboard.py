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
        tile_id = request.env['dashboard.block'].sudo().browse(int(kw.get('id')))
        if tile_id:
            domain = ast.literal_eval(tile_id.filter) if tile_id.filter else []

            # Only apply date filters if filter_bool is True
            if tile_id.filter_bool:
                start_date = kw.get('start_date')
                end_date = kw.get('end_date')

                if start_date and end_date:
                    try:
                        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(hours=23, minutes=59, seconds=59)
                        domain.append(('create_date', '>=', start_dt))
                        domain.append(('create_date', '<=', end_dt))
                    except Exception as e:
                        _logger.error(f"Date parse error: {e}")

            # Else fallback to saved time_period field (optional)
            elif tile_id.time_period:
                today = datetime.today()
                if tile_id.time_period == 'today':
                    start = today.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = today.replace(hour=23, minute=59, second=59, microsecond=999999)
                    domain += [('create_date', '>=', start), ('create_date', '<=', end)]
                elif tile_id.time_period == 'week':
                    start = today - timedelta(days=today.weekday())
                    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
                    end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
                    domain += [('create_date', '>=', start), ('create_date', '<=', end)]
                elif tile_id.time_period == 'month':
                    start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    next_month = today.replace(day=28) + timedelta(days=4)
                    end = next_month.replace(day=1, hour=23, minute=59, second=59, microsecond=999999) - timedelta(
                        days=1)
                    domain += [('create_date', '>=', start), ('create_date', '<=', end)]
                elif tile_id.time_period == 'year':
                    start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                    end = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                    domain += [('create_date', '>=', start), ('create_date', '<=', end)]

            _logger.info(f'============ DOMAIN: {domain} =====================')
            return {
                'model': tile_id.model_id.model,
                'model_name': tile_id.model_id.name,
                'filter': domain
            }

        return False

    @http.route('/custom_dashboard/search_input_chart', type='json',
                auth="public", website=True)
    def dashboard_search_input_chart(self, search_input):
        """Function to filter search input in dashboard"""
        return request.env['dashboard.block'].search([
            ('name', 'ilike', search_input)]).ids

