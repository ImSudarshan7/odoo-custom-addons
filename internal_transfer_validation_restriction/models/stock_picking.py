# models/stock_picking.py
from odoo import models, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def button_validate(self):
        if self.picking_type_id.code == 'internal':
            allowed_users = self.location_dest_id.allowed_user_ids
            if self.env.user not in allowed_users:
                raise ValidationError(
                    "You are not allowed to validate this transfer. Only users assigned to the destination location can validate.")
        return super(StockPicking, self).button_validate()
