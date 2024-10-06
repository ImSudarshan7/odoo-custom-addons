from odoo import models, api
# from odoo.exceptions import AccessError

class ProductTemplate(models.Model):
    _inherit = 'product.template'
#
#     # @api.model
#     # def check_access_rights(self, operation, raise_exception=True):
#     #     if operation in ('read', 'write') and not self.env.user.has_group('my_module.group_product_extra_info'):
#     #         if raise_exception:
#     #             raise AccessError("You don't have access to this information.")
#     #         return False
#     #     return super(ProductTemplate, self).check_access_rights(operation, raise_exception)
