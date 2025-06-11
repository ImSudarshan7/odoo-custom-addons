from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Override to prevent stock.picking creation from sale order confirmation
        for stockable products.
        The original method in 'sale_stock' module creates procurements
        which in turn generate pickings.
        """
        stockable_lines = self.filtered(lambda l: l.product_id.type == 'product')
        non_stockable_lines = self - stockable_lines

        if non_stockable_lines:
            super(SaleOrderLine, non_stockable_lines)._action_launch_stock_rule(
                previous_product_uom_qty=previous_product_uom_qty)

        return True


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sales_location = fields.Selection([
        ('ktm', 'Kathmandu Office'),
        ('sif', 'Simara Office')
    ], string='Sales Location', copy=True, required=True
    )





def _prepare_invoice(self):
    """
    Prepare the dict of values to create the new invoice for a sales order.
    This method may be overridden to implement custom invoice generation
    (making sure to call super() to establish a clean extension chain).
    """
    invoice_vals = super(SaleOrder, self)._prepare_invoice()

    if self.sales_location:
        invoice_vals.update({
            'invoice_location': self.sales_location,
        })

    return invoice_vals


def _create_invoices(self, grouped=False, final=False):  # Older Odoo signature

    invoices = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)

    return invoices
