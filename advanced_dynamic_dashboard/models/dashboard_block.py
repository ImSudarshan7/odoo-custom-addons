from ast import literal_eval
from datetime import datetime
from odoo import api, fields, models
from odoo.osv import expression
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class DashboardBlock(models.Model):
    """Class is used to create charts and tiles in dashboard"""
    _name = "dashboard.block"
    _description = "Dashboard Blocks"

    def get_default_action(self):
        """Function to get values from dashboard if action_id is true return
        id else return false"""
        action_id = self.env.ref(
            'advanced_dynamic_dashboard.dashboard_view_action')
        if action_id:
            return action_id.id
        return False



    group_id = fields.Many2one('res.groups', string="Visible for Group",domain=lambda self: [('category_id', '=', self.env.ref('advanced_dynamic_dashboard.category_ticket_management_dashboard').id)]
    )

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Employee',default=lambda self: self.env.user.employee, tracking=True)
    _logger.info(f'============={employee_id}========hh=============')

    name = fields.Char(string="Name", help='Name of the block')
    fa_icon = fields.Char(string="Icon", help="Add icon for tile")
    graph_size = fields.Selection(
        selection=[("col-lg-4", "Small"), ("col-lg-6", "Medium"),
                   ("col-lg-12", "Large")],
        string="Graph Size", default='col-lg-4', help="Select the graph size")
    operation = fields.Selection(
        selection=[("sum", "Sum"), ("avg", "Average"), ("count", "Count")],
        string="Operation",
        help='Tile Operation that needs to bring values for tile',
        required=True)
    graph_type = fields.Selection(
        selection=[("bar", "Bar"), ("radar", "Radar"), ("pie", "Pie"),
                   ("line", "Line"),
                   ("doughnut", "Doughnut")],
        string="Chart Type", help='Type of Chart')
    measured_field_id = fields.Many2one("ir.model.fields",
                                        string="Measured Field",
                                        help="Select the Measured")
    client_action_id = fields.Many2one('ir.actions.client',
                                       string="Client action",
                                       default=get_default_action,
                                       help="Choose the client action")
    type = fields.Selection(
        selection=[("graph", "Chart"), ("tile", "Tile")], string="Type",
        help='Type of Block ie, Chart or Tile')
    x_axis = fields.Char(string="X-Axis", help="Chart X-axis")
    y_axis = fields.Char(string="Y-Axis", help="Chart Y-axis")
    x_pos = fields.Integer(string="X-Position", help="Chart X-axis position")
    y_pos = fields.Integer(string="Y-Position", help="Chart Y-axis position")
    height = fields.Integer(string="Height", help="Chart height")
    width = fields.Integer(string="Width", help="Chart width")
    group_by_id = fields.Many2one("ir.model.fields", store=True,
                                  string="Group by(Y-Axis)",
                                  help='Field value for Y-Axis')
    tile_color = fields.Char(string="Tile Color", help='Primary color of Tile')
    text_color = fields.Char(string="Text Color", help='Text color of Tile')
    val_color = fields.Char(string="Value Color", help='Value color of Tile')
    fa_color = fields.Char(string="Icon Color", help='Icon color of Tile')
    filter = fields.Char(string="Filter", help="Add filter")
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        help="Select the module name",
        default=lambda self: self.env['ir.model'].search([('model', '=', 'ticket.management')], limit=1).id
    )
    model_name = fields.Char(related='model_id.model', string="Model Name",
                             help="Added model_id model")

    edit_mode = fields.Boolean(string="Edit Mode",
                               help="Enable to edit chart and tile",
                               invisible=True)

    time_period = fields.Selection(
        [('today', 'Today'),
         ('week', 'This Week'),
         ('month', 'This Month'),
         ('year', 'This Year')],
        string='Time Period',
    )
    filter_bool = fields.Boolean(string="Filter",default=True,)

    @api.onchange('model_id')
    def _onchange_model_id(self):
        """Method to work when the value in the field model_id changes"""
        self.operation = False
        self.measured_field_id = False
        self.group_by_id = False

    def get_dashboard_vals(self, action_id, start_date=None, end_date=None,):
        """Fetch block values from js and create chart"""
        block_id = []
        user = self.env.user
        company_id=self.env.company
        is_admin = user.has_group('advanced_dynamic_dashboard.dashboard_group_admin')
        # Get the specific block if a block ID is provided
        blocks = self.sudo().search([('client_action_id', '=', int(action_id))])
        if isinstance(action_id, list) and len(action_id) == 1:
            blocks = blocks.filtered(lambda r: r.id == action_id[0])

        for rec in blocks:
            if rec.group_id and rec.group_id not in user.groups_id:
                continue

            if rec.filter is False:
                rec.filter = "[]"

            filter_list = literal_eval(rec.filter)

            # Remove existing date filters if any exist
            filter_list = [filter_item for filter_item in filter_list if not (
                    isinstance(filter_item, tuple) and filter_item[0] ==
                    'create_date')]

            # Only apply date filters if filter_bool is True
            if rec.filter_bool:
                if start_date and start_date != 'null':
                    start_date_obj = datetime.strptime(start_date,
                                                       '%Y-%m-%d')
                    filter_list.append(
                        ('create_date', '>=', start_date_obj.strftime('%Y-%m-%d')))
                if end_date and end_date != 'null':
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                    filter_list.append(
                        ('create_date', '<=', end_date_obj.strftime('%Y-%m-%d')))
            rec.filter = repr(filter_list)

            vals = {'id': rec.id,
                    'name': rec.name,
                    'type': rec.type,
                    'graph_type': rec.graph_type,
                    'icon': rec.fa_icon,
                    'cols': rec.graph_size,
                    'filter_bool': rec.filter_bool,
                    'color': 'background-color: %s;' % rec.tile_color

                    if rec.tile_color else '#1f6abb;',
                    'text_color': 'color: %s;' % rec.text_color

                    if rec.text_color else '#FFFFFF;',
                    'val_color': 'color: %s;' % rec.val_color

                    if rec.val_color else '#FFFFFF;',
                    'icon_color': 'color: %s;' % rec.tile_color

                    if rec.tile_color else '#1f6abb;',
                    'x_pos': rec.x_pos, 'y_pos': rec.y_pos,
                    'height': rec.height,
                    'width': rec.width}

            domain = []

            if rec.filter:
                domain = expression.AND([literal_eval(rec.filter)])
            # Add time_period filter only if filter_bool is True
            if rec.time_period and rec.filter_bool:
                today = datetime.today()
                if rec.time_period == 'today':
                    start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_of_today = today.replace(hour=23, minute=59, second=59, microsecond=999999)
                    domain = expression.AND(
                        [domain, [('create_date', '>=', start_of_today), ('create_date', '<=', end_of_today)]])

                elif rec.time_period == 'week':
                    start_of_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0,
                                                                                      microsecond=0)
                    end_of_week = (start_of_week + timedelta(days=6)).replace(hour=23, minute=59, second=59,
                                                                              microsecond=999999)
                    domain = expression.AND(
                        [domain, [('create_date', '>=', start_of_week), ('create_date', '<=', end_of_week)]])

                elif rec.time_period == 'month':
                    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    next_month = (start_of_month + timedelta(days=32)).replace(day=1)
                    end_of_month = (next_month - timedelta(days=1)).replace(hour=23, minute=59, second=59,
                                                                            microsecond=999999)
                    domain = expression.AND(
                        [domain, [('create_date', '>=', start_of_month), ('create_date', '<=', end_of_month)]])

                elif rec.time_period == 'year':
                    start_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                    end_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
                    domain = expression.AND(
                        [domain, [('create_date', '>=', start_of_year), ('create_date', '<=', end_of_year)]])

            if company_id:
                domain = expression.AND([domain, [('company_id', '=', company_id.id)]])

            if rec.model_name:
                if rec.type == 'graph':
                    query, params, *_ = self.env[rec.model_name].get_query(
                        domain,
                        rec.operation,
                        rec.measured_field_id,
                        group_by=rec.group_by_id if rec.type == 'graph' else None
                    )
                    self._cr.execute(query, params)

                    records = self._cr.dictfetchall()
                    x_axis, y_axis = [], []
                    for record in records:
                        name = record.get('name')
                        if isinstance(name, dict):
                            name = name.get(self._context.get('lang') or 'en_US', str(name))
                        x_axis.append(name or 'N/A')  
                        y_axis.append(record.get('value') or 0)

                    vals.update({
                        'x_axis': x_axis,
                        'y_axis': y_axis,
                    })

                else:
                    query, params, *_ = self.env[rec.model_name].get_query(
                        domain, rec.operation, rec.measured_field_id
                    )
                    self._cr.execute(query, params)
                    records = self._cr.dictfetchall()

                    total = records[0].get('value')
                    val = total
                    records[0]['value'] = val
                    vals.update(records[0])
            block_id.append(vals)
        return {
            'block_id': block_id,
            'is_admin': is_admin,
        }

    def get_save_layout(self, act_id, grid_data_list):
        """Function fetch edited values while edit layout of the chart or tile
         and save values in a database"""
        for block in self.env['dashboard.block'].sudo().search(
                [('client_action_id', '=', int(act_id))]):
            for data in grid_data_list:
                if block['id'] == data['id']:
                    block.write({
                        'x_pos': int(data['x']),
                        'y_pos': int(data['y']),
                        'height': int(data['height']),
                        'width': int(data['width']),
                    })
