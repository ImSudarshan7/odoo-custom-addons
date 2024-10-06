# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
from io import StringIO
from odoo import api, fields, models
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning

import logging
_logger = logging.getLogger(__name__)
import io
try:
    import xlwt
except ImportError:
    xlwt = None


class sale_day_book_wizard(models.TransientModel):
    _name = "sale.day.book.wizard"

    start_date = fields.Date('Start Period', required=True)
    end_date = fields.Date('End Period', required=True)
    warehouse = fields.Many2many('stock.warehouse', 'wh_wiz_rel_inv_val', 'wh', 'wiz', string='Warehouse')
    category = fields.Many2many('product.category', 'categ_wiz_rel', 'categ', 'wiz')
    location_id = fields.Many2one('stock.location', string='Location')
    company_id = fields.Many2one('res.company', string='Company')
    display_sum = fields.Boolean("Summary")
    filter_by = fields.Selection([('product', 'Product'), ('categ', 'Category')], string="Filter By", default="product")
    product_ids = fields.Many2many('product.product', 'rel_product_val_wizard', string="Product")

    def print_report(self):
        datas = {
            'ids': self._ids,
            'model': 'sales.day.book.wizard',
            'start_date': self.start_date,
            'end_date': self.end_date,
            'warehouse': self.warehouse,
            'company_id': self.company_id,
            'display_sum': self.display_sum,
            'product_ids': self.product_ids,
            'filter_by': self.filter_by
            }
        return self.env.ref('bi_inventory_valuation_reports.inventory_product_category_template_pdf').report_action(self)

    def get_warehouse(self):
        if self.warehouse:
            l1 = []
            l2 = []
            for i in self.warehouse:
                obj = self.env['stock.warehouse'].search([('id', '=', i.id)])
                for j in obj:
                    l2.append(j.id)
            return l2
        return []

    def _get_warehouse_name(self):
        if self.warehouse:
            l1 = []
            l2 = []
            for i in self.warehouse:
                obj = self.env['stock.warehouse'].search([('id', '=', i.id)])
                l1.append(obj.name)
                myString = ",".join(l1 )
            return myString
        return ''

    def get_company(self):
        if self.company_id:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            l1.append(obj.name)
            return l1

    def get_currency(self):
        if self.company_id:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            l1.append(obj.currency_id.name)
            return l1

    def get_category(self):
        if self.category:
            l2 = []
            obj = self.env['product.category'].search([('id', 'in', self.category)])
            for j in obj:
                l2.append(j.id)
            return l2
        return ''

    def get_date(self):
        date_list = []
        obj = self.env['stock.history'].search([('date', '>=', self.start_date), ('date', '<=', self.end_date)])
        for j in obj:
            date_list.append(j.id)
        return date_list

    def _compute_quantities_product_quant_dic(self, lot_id, owner_id, package_id, from_date, to_date, product_obj, data):
        loc_list = []
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product_obj._get_domain_locations()
        custom_domain = []
        if data['company_id']:
            obj = self.env['res.company'].search([('name', '=', data['company_id'])])
            custom_domain.append(('company_id', '=', obj.id))

        if data['location_id']:
            custom_domain.append(('location_id', '=', data['location_id'].id))

        if data['warehouse']:
            ware_check_domain = [a.id for a in data['warehouse']]
            locations = []
            for i in ware_check_domain:

                loc_ids = self.env['stock.warehouse'].search([('id', '=', i)])

                locations.append(loc_ids.view_location_id.id)
                for i in loc_ids.view_location_id.child_ids:
                  locations.append(i.id)

                loc_list.append(loc_ids.lot_stock_id.id)

            custom_domain.append(('location_id', 'in', locations))

        domain_quant = [('product_id', 'in', product_obj.ids)] + domain_quant_loc + custom_domain
        #print ("dddddddddddddddddddddddddddddddddddddddddd",domain_quant)
        dates_in_the_past = False
        # only to_date as to_date will correspond to qty_available
        #to_date = fields.Datetime.to_datetime(to_date)

        if to_date and to_date < date.today():

            dates_in_the_past = True

        domain_move_in = [('product_id', 'in', product_obj.ids)] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', product_obj.ids)] + domain_move_out_loc
        if lot_id is not None:
            domain_quant += [('lot_id', '=', lot_id)]
        if owner_id is not None:
            domain_quant += [('owner_id', '=', owner_id)]
            domain_move_in += [('restrict_partner_id', '=', owner_id)]
            domain_move_out += [('restrict_partner_id', '=', owner_id)]
        if package_id is not None:
            domain_quant += [('package_id', '=', package_id)]
        if dates_in_the_past:
            domain_move_in_done = list(domain_move_in)
            domain_move_out_done = list(domain_move_out)
        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]

        Move = self.env['stock.move']
        Quant = self.env['stock.quant']
        domain_move_in_todo = [('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
        domain_move_out_todo = [('state', 'in', ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out
        moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
        moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
        quants_res = dict((item['product_id'][0], item['quantity']) for item in Quant.read_group(domain_quant, ['product_id', 'quantity'], ['product_id'], orderby='id'))

        if dates_in_the_past:
            # Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
            domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
            domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
            moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_in_done, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
            moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_out_done, ['product_id', 'product_qty'], ['product_id'], orderby='id'))

        res = dict()
        for product in product_obj.with_context(prefetch_fields=False):
            product_id = product.id
            rounding = product.uom_id.rounding
            res[product_id] = {}
            if dates_in_the_past:
                qty_available = quants_res.get(product_id, 0.0) - moves_in_res_past.get(product_id, 0.0) + moves_out_res_past.get(product_id, 0.0)
            else:
                qty_available = quants_res.get(product_id, 0.0)
            res[product_id]['qty_available'] = float_round(qty_available, precision_rounding=rounding)
            res[product_id]['incoming_qty'] = float_round(moves_in_res.get(product_id, 0.0), precision_rounding=rounding)
            res[product_id]['outgoing_qty'] = float_round(moves_out_res.get(product_id, 0.0), precision_rounding=rounding)
            res[product_id]['virtual_available'] = float_round(
                qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'],
                precision_rounding=rounding)

        return res

    def get_lines(self, data):
            product_res = self.env['product.product'].search([('qty_available', '!=', 0),
                                                                ('type', '=', 'product')])
            category_lst = []
            if data['category']:

                for cate in data['category'] and data['filter_by'] == 'categ':
                    if cate.id not in category_lst:
                       category_lst.append(cate.id)

                    for child in cate.child_id:
                        if child.id not in category_lst :
                            category_lst.append(child.id)

            if len(category_lst) > 0:

                product_res = self.env['product.product'].search([('categ_id', 'in', category_lst),('qty_available', '!=', 0), ('type', '=', 'product')])

            if data['product_ids'] and data['filter_by'] == 'product':
                product_res = data['product_ids']

            lines = []
            for product in product_res:

                #if product.create_date.date() <= data['start_date'] :

                sales_value = 0.0
                incoming = 0.0

                opening = self._compute_quantities_product_quant_dic(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), False, data['start_date'], product, data)

                #ending = self._compute_quantities_product_quant_dic(False,data['end_date'],product,data)

                #if opening[product.id]['qty_available'] > 0 :

                custom_domain = []
                if data['company_id']:
                    obj = self.env['res.company'].search([('name', '=', data['company_id'])])

                    custom_domain.append(('company_id','=',obj.id))

                if data['warehouse'] :
                    warehouse_lst = [a.id for a in data['warehouse']]
                    custom_domain.append(('picking_id.picking_type_id.warehouse_id','in',warehouse_lst))

                stock_move_line = self.env['stock.move'].search([
                    ('product_id', '=', product.id),
                    ('picking_id.date_done', '>', data['start_date']),
                    ('picking_id.date_done', "<=", data['end_date']),
                    ('state', '=', 'done')
                    ] + custom_domain)

                for move in stock_move_line:
                    if move.picking_id.picking_type_id.code == "outgoing":
                        if data['location_id']:
                            locations_lst = [data['location_id'].id]
                            for i in data['location_id'].child_ids:
                                locations_lst.append(i.id)
                            if move.location_id.id in locations_lst:
                                sales_value += move.product_uom_qty
                        else:
                            sales_value += move.product_uom_qty

                    if move.picking_id.picking_type_id.code == "incoming":
                        if data['location_id']:
                            locations_lst = [data['location_id'].id]
                            for i in data['location_id'].child_ids:
                                locations_lst.append(i.id)
                            if move.location_dest_id.id in locations_lst:
                                incoming += move.product_uom_qty
                        else:
                            incoming += move.product_uom_qty

                stock_val_layer = self.env['stock.valuation.layer'].search([
                        ('product_id', '=', product.id),
                        ('create_date', '>=', data['start_date']),
                        ('create_date', "<=", data['end_date']),

                        ])

                cost = 0
                count = 0
                for layer in stock_val_layer:
                    if layer.stock_move_id.picking_id.picking_type_id.code == "incoming":
                        cost = cost + layer.unit_cost
                        count = count + 1

                    if not layer.stock_move_id.picking_id:
                        cost = cost + layer.unit_cost
                        count = count + 1

                avg_cost = 0
                if count > 0:
                    avg_cost = cost / count

                if avg_cost == 0:
                    avg_cost = product.standard_price

                inventory_domain = [('date', '>=', data['start_date']), ('date', "<=", data['end_date'])]

                stock_pick_lines = self.env['stock.move'].search([('location_id.usage', '=', 'inventory'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_internal_lines = self.env['stock.move'].search([('location_id.usage', '=', 'inventory'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_internal_lines_2 = self.env['stock.move'].search([('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'inventory'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_production_in = self.env['stock.move'].search([('state','=','done'),('location_id.usage', '=', 'production'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_production_out = self.env['stock.move'].search([('state','=','done'),('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'production'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_sales = self.env['stock.move'].search([('state','=','done'),('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'customer'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_sales_return = self.env['stock.move'].search([('state','=','done'),('location_id.usage', '=', 'customer'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_purchase = self.env['stock.move'].search([('state','=','done'),('location_id.usage', '=', 'supplier'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
                stock_purchase_return = self.env['stock.move'].search([('state','=','done'),('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'supplier'),('product_id.id', '=', product.id)] + inventory_domain)

                adjust = 0
                internal = 0
                plus_picking = 0
                production_in = 0.0
                production_out = 0.0
                adjustment_in = 0.0
                adjustment_out = 0.0
                sales = 0.0
                sales_return = 0.0
                purchase = 0.0
                purchase_return = 0.0

                if stock_pick_lines:
                    for invent in stock_pick_lines:
                        adjust = invent.product_uom_qty
                        plus_picking = invent.id

                min_picking = 0

                if stock_internal_lines_2:
                    for inter in stock_internal_lines_2:
                        plus_min = inter.product_uom_qty
                        min_picking = inter.id

                if plus_picking > min_picking:
                    picking_id = self.env['stock.move'].browse(plus_picking)
                    adjust = picking_id.product_uom_qty
                else:
                    picking_id = self.env['stock.move'].browse(min_picking)
                    adjust = -int(picking_id.product_uom_qty)

                if stock_internal_lines:
                    for inter in stock_internal_lines:
                        adjustment_in += inter.product_uom_qty

                if stock_internal_lines_2:
                    for inter in stock_internal_lines_2:
                        adjustment_out += inter.product_uom_qty

                if stock_production_in:
                    for prod_in in stock_production_in:
                        production_in += prod_in.product_uom_qty

                if stock_production_out:
                    for prod_out in stock_production_out:
                        production_out += prod_out.product_uom_qty

                if stock_sales:
                    for sale in stock_sales:
                        sales += sale.product_uom_qty

                if stock_sales_return:
                    for sale_return in stock_sales_return:
                        sales_return += sale_return.product_uom_qty

                if stock_purchase:
                    for pur in stock_purchase:
                        purchase += pur.product_uom_qty

                if stock_purchase_return:
                    for pur_return in stock_purchase_return:
                        purchase_return += pur_return.product_uom_qty

                ending_bal = opening[product.id]['qty_available'] - sales + sales_return + purchase - purchase_return + adjustment_in - adjustment_out + production_in - production_out

                method = ''
                price_used = product.standard_price
                if product.categ_id.property_cost_method == 'average':
                    method = 'Average Cost (AVCO)'
                    price_used = avg_cost

                elif product.categ_id.property_cost_method == 'standard':
                    method = 'Standard Price'
                    price_used = product.standard_price

                vals = {
                        'sku': product.default_code or '',
                        'name': product.name or '',
                        'category': product.categ_id.name or '',
                        'cost_price': price_used or 0,
                        'available':  0,
                        'virtual':   0,
                        'incoming': incoming or 0,
                        'outgoing':  adjust,
                        'net_on_hand':   ending_bal,
                        'total_value': ending_bal * price_used or 0,
                        'sale_value': sales_value or 0,
                        'sales': sales or 0,
                        'sales_return': sales_return or 0,
                        'purchase': purchase or 0,
                        'purchase_return': purchase_return or 0,
                        'production_in': production_in or 0,
                        'production_out': production_out or 0,
                        'adjustment_in': adjustment_in or 0,
                        'adjustment_out': adjustment_out or 0,
                        'purchase_value':  0,
                        'beginning': opening[product.id]['qty_available'] or 0,
                        'internal': internal,
                        'costing_method': method,
                        'barcode': product.barcode or '',
                    }
                lines.append(vals)

            return lines

    def get_data(self, data):
        product_res = self.env['product.product'].search([('qty_available', '!=', 0), ('type', '=', 'product')])
        category_lst = []
        if data['category']:

            for cate in data['category']:
                if cate.id not in category_lst:
                   category_lst.append(cate.id)

                for child in cate.child_id :
                    if child.id not in category_lst:
                        category_lst.append(child.id)

        if len(category_lst) > 0:

            product_res = self.env['product.product'].search([('categ_id', 'in', category_lst), ('qty_available', '!=', 0), ('type', '=', 'product')])

        lines = []
        for product in product_res:
            #if product.create_date.date() <= data['start_date'] :

            sales_value = 0.0
            incoming = 0.0

            opening = self._compute_quantities_product_quant_dic(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'),False,data['start_date'],product,data)

            #ending = self._compute_quantities_product_quant_dic(False,data['end_date'],product,data)

            #if opening[product.id]['qty_available'] > 0 :

            #print ("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",ending)
            custom_domain = []
            if data['company_id']:
                obj = self.env['res.company'].search([('name', '=', data['company_id'])])

                custom_domain.append(('company_id', '=', obj.id))

            if data['warehouse']:
                warehouse_lst = [a.id for a in data['warehouse']]
                custom_domain.append(('picking_id.picking_type_id.warehouse_id', 'in', warehouse_lst))

            stock_move_line = self.env['stock.move'].search([
                ('product_id', '=', product.id),
                ('picking_id.date_done', '>=', data['start_date']),
                ('picking_id.date_done', "<=", data['end_date']),
                ('state', '=', 'done')
                ] + custom_domain)

            for move in stock_move_line:
                if move.picking_id.picking_type_id.code == "outgoing":
                    if data['location_id'] :
                        locations_lst = [data['location_id'].id]
                        for i in data['location_id'].child_ids:
                            locations_lst.append(i.id)
                        if move.location_id.id in locations_lst:
                            sales_value += move.product_uom_qty
                    else:
                        sales_value += move.product_uom_qty

                if move.picking_id.picking_type_id.code == "incoming":
                    if data['location_id']:
                        locations_lst = [data['location_id'].id]
                        for i in data['location_id'].child_ids:
                            locations_lst.append(i.id)
                        if move.location_dest_id.id in locations_lst:
                            incoming += move.product_uom_qt
                    else:
                        incoming += move.product_uom_qty

            stock_val_layer = self.env['stock.valuation.layer'].search([
                    ('product_id', '=', product.id),
                    ('create_date', '>=', data['start_date']),
                    ('create_date', "<=", data['end_date']),
                    ])

            cost = 0
            count = 0
            for layer in stock_val_layer:
                if layer.stock_move_id.picking_id.picking_type_id.code == "incoming":
                    cost = cost + layer.unit_cost
                    count = count + 1

                if not layer.stock_move_id.picking_id:
                    cost = cost + layer.unit_cost
                    count = count + 1

            avg_cost = 0

            if count > 0:
                avg_cost = cost / count

            if avg_cost == 0:
                avg_cost = product.standard_price

            inventory_domain = [
                ('date', '>=', data['start_date']),
                ('date', "<=", data['end_date'])
                ]
            # stock_picking = self.env['stock.picking'].search([('state','=','done')])
            stock_pick_lines = self.env['stock.move'].search([('location_id.usage', '=', 'inventory'), ('product_id.id', '=', product.id)] + inventory_domain)
            stock_internal_lines = self.env['stock.move'].search([('location_id.usage', '=', 'inventory'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id','=',product.id)] + inventory_domain)
            stock_internal_lines_2 = self.env['stock.move'].search([('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'inventory'), ('product_id.id','=',product.id)] + inventory_domain)
            stock_production_in = self.env['stock.move'].search([('location_id.usage', '=', 'production'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
            stock_production_out = self.env['stock.move'].search([('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'production'), ('product_id.id', '=', product.id)] + inventory_domain)
            stock_sales = self.env['stock.move'].search([('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'customer'), ('product_id.id', '=', product.id)] + inventory_domain)
            stock_sales_return = self.env['stock.move'].search([('location_id.usage', '=', 'customer'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
            stock_purchase = self.env['stock.move'].search([('location_id.usage', '=', 'supplier'),('state','=','done'), ('location_dest_id.usage', '=', 'internal'), ('product_id.id', '=', product.id)] + inventory_domain)
            stock_purchase_return = self.env['stock.move'].search([('location_id.usage', '=', 'internal'), ('location_dest_id.usage', '=', 'supplier'), ('product_id.id', '=', product.id)] + inventory_domain)

            adjust = 0
            internal = 0
            plus_picking = 0
            production_in = 0
            production_out = 0
            adjustment_in = 0
            adjustment_out = 0
            sales = 0
            sales_return = 0
            purchase = 0
            purchase_return = 0

            if stock_pick_lines:
                for invent in stock_pick_lines:

                    adjust = invent.product_uom_qty
                    plus_picking = invent.id

            min_picking = 0
            if stock_internal_lines_2:
                for inter in stock_internal_lines_2:
                    #print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",inter)
                    plus_min = inter.product_uom_qty
                    min_picking = inter.id

                    #print("plus_min==================================",plus_min)

            if plus_picking > min_picking:
                picking_id = self.env['stock.move'].browse(plus_picking)
                adjust = picking_id.product_uom_qty
            else:
                picking_id = self.env['stock.move'].browse(min_picking)
                adjust = -int(picking_id.product_uom_qty)

            if stock_internal_lines:
                for inter in stock_internal_lines:
                    adjustment_in += inter.product_uom_qty

            if stock_internal_lines_2:
                for inter in stock_internal_lines_2:
                    adjustment_out += inter.product_uom_qty

            if stock_production_in:
                for prod_in in stock_production_in:
                    production_in += prod_in.product_uom_qty

            if stock_production_out:
                for prod_out in stock_production_out:
                    production_out += prod_out.product_uom_qty

            if stock_sales:
                for sale in stock_sales:
                    sales += sale.product_uom_qty

            if stock_sales_return:
                for sale_return in stock_sales_return:
                    sales_return += sale_return.product_uom_qty

            if stock_purchase:
                _logger.info("=====================%s==",stock_purchase)
                for pur in stock_purchase:
                    purchase += pur.product_uom_qty

            if stock_purchase_return:
                for pur_return in stock_purchase_return:
                    purchase_return += pur_return.product_uom_qty

            ending_bal = opening[product.id]['qty_available'] - sales + sales_return + purchase - purchase_return + adjustment_in - adjustment_out + production_in - production_out

            method = ''
            price_used = product.standard_price
            barcode = product.barcode
            if product.categ_id.property_cost_method == 'average':
                method = 'Average Cost (AVCO)'
                price_used = avg_cost

            elif product.categ_id.property_cost_method == 'standard':
                method = 'Standard Price'
                price_used = product.standard_price

            flag = False
            for i in lines:
                if i['category'] == product.categ_id.name:
                    i['beginning'] = i['beginning'] + opening[product.id]['qty_available']
                    i['internal'] = i['internal'] + internal
                    # i['incoming'] = i['incoming'] + incoming
                    # i['sale_value'] = i['sale_value'] + sales_value
                    # i['outgoing'] = i['outgoing'] + adjust
                    i['sales'] = i['sales'] + sales
                    i['sales_return'] = i['sales_return'] + sales_return
                    i['purchase'] = i['purchase'] + purchase
                    i['purchase_return'] = i['purchase_return'] + purchase_return
                    i['adjustment_in'] = i['adjustment_in'] + adjustment_in
                    i['adjustment_out'] = i['adjustment_out'] + adjustment_out
                    i['production_in'] = i['production_in'] + production_in
                    i['production_out'] = i['production_out'] + production_out
                    i['net_on_hand'] = i['net_on_hand'] + ending_bal
                    i['total_value'] = i['total_value'] + (ending_bal * price_used)
                    flag = True

            if not flag:

                vals = {
                    'category': product.categ_id.name,
                    'cost_price': price_used or 0,
                    'available':  0,
                    'virtual':  0,
                    'incoming': incoming or 0,
                    'outgoing': adjust or 0,
                    'net_on_hand': ending_bal or 0,
                    'total_value': ending_bal * price_used or 0,
                    'sale_value': sales_value or 0,
                    'purchase_value':  0,
                    'beginning': opening[product.id]['qty_available'] or 0,
                    'internal': internal or 0,
                    'sales': sales or 0,
                    'sales_return': sales_return or 0,
                    'purchase': purchase or 0,
                    'purchase_return': purchase_return or 0,
                    'production_in': production_in or 0,
                    'production_out': production_out or 0,
                    'adjustment_in': adjustment_in or 0,
                    'adjustment_out': adjustment_out or 0,
                    'barcode': barcode or 0,
                }
                lines.append(vals)
        return lines

    def print_exl_report(self):
        if xlwt:
            data = {'start_date': self.start_date,
                    'end_date': self.end_date, 'warehouse': self.warehouse,
                    'category': self.category,
                    'location_id': self.location_id,
                    'company_id': self.company_id.name,
                    'display_sum': self.display_sum,
                    'currency': self.company_id.currency_id.name,
                    'product_ids': self.product_ids,
                    'filter_by': self.filter_by
                    }
            filename = 'Stock Valuation Report.xls'
            get_warehouse = self.get_warehouse()
            get_warehouse_name = self._get_warehouse_name()
            l1 = []
            get_company = self.get_company()
            get_currency = self.get_currency()
            workbook = xlwt.Workbook()
            stylePC = xlwt.XFStyle()
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            fontP = xlwt.Font()
            fontP.bold = True
            fontP.height = 200
            stylePC.font = fontP
            stylePC.num_format_str = '@'
            stylePC.alignment = alignment
            style_title = xlwt.easyxf("font:height 300; font: name Liberation Sans, bold on,color blue; align: horiz center")
            style_table_header = xlwt.easyxf("font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
            style = xlwt.easyxf("font:height 200; font: name Liberation Sans,color black;")
            worksheet = workbook.add_sheet('Sheet 1')
            worksheet.write(3, 0, 'Start Date:', style_table_header)
            worksheet.write(4, 0, str(self.start_date))
            worksheet.write(3, 1, 'End Date', style_table_header)
            worksheet.write(4, 1, str(self.end_date))
            worksheet.write(3, 2, 'Company', style_table_header)
            worksheet.write(4, 2, get_company and get_company[0] or '',)
            worksheet.write(3, 3, 'Warehouse(s)', style_table_header)
            worksheet.write(3, 4, 'Currency', style_table_header)
            worksheet.write(4, 4, get_currency and get_currency[0] or '',)
            w_col_no = 7
            w_col_no1 = 8
            if get_warehouse_name:
                   # w_col_no = w_col_no + 8
                worksheet.write(4, 3, get_warehouse_name, stylePC)
                   # w_col_no1 = w_col_no1 + 9
            if self.display_sum:
                worksheet.write_merge(0, 1, 1, 11, "Inventory Valuation Summary Report", style=style_title)
                worksheet.write(6, 0, 'Category', style_table_header)
                worksheet.write(6, 1, 'Beginning', style_table_header)
                worksheet.write(6, 2, 'Internal', style_table_header)
                worksheet.write(6, 3, 'Purchase', style_table_header)
                worksheet.write(6, 4, 'Purchase Return', style_table_header)
                worksheet.write(6, 5, 'Sales', style_table_header)
                worksheet.write(6, 6, 'Sales Return', style_table_header)
                worksheet.write(6, 7, 'Adjustment In', style_table_header)
                worksheet.write(6, 8, 'Adjustment Out', style_table_header)
                worksheet.write(6, 9, 'Production In', style_table_header)
                worksheet.write(6, 10, 'Production Out', style_table_header)
                worksheet.write(6, 11, 'Ending', style_table_header)
                worksheet.write(6, 12, 'Valuation', style_table_header)
                prod_row = 7
                prod_col = 0

                get_line = self.get_data(data)
                for each in get_line:
                    worksheet.write(prod_row, prod_col, each['category'], style)
                    worksheet.write(prod_row, prod_col+1, each['beginning'], style)
                    worksheet.write(prod_row, prod_col+2, each['internal'], style)

                    worksheet.write(prod_row, prod_col+3, each['purchase'], style)
                    worksheet.write(prod_row, prod_col+4, each['purchase_return'], style)
                    worksheet.write(prod_row, prod_col+5, each['sales'], style)
                    worksheet.write(prod_row, prod_col+6, each['sales_return'], style)
                    worksheet.write(prod_row, prod_col+7, each['adjustment_in'], style)
                    worksheet.write(prod_row, prod_col+8, each['adjustment_out'], style)
                    worksheet.write(prod_row, prod_col+9, each['production_in'], style)
                    worksheet.write(prod_row, prod_col+10, each['production_out'], style)

                    worksheet.write(prod_row, prod_col+11, each['net_on_hand'], style)
                    worksheet.write(prod_row, prod_col+12, each['total_value'], style)
                    prod_row = prod_row + 1

                prod_row = 8
                prod_col = 7
            else:
                worksheet.write_merge(0, 1, 2, 15, "Inventory Valuation Report", style=style_title)
                worksheet.write(6, 0, 'Default Code', style_table_header)
                worksheet.write(6, 1, 'Barcode', style_table_header)
                worksheet.write(6, 2, 'Name', style_table_header)
                worksheet.write(6, 3, 'Category', style_table_header)
                worksheet.write(6, 4, 'Costing Method', style_table_header)
                worksheet.write(6, 5, 'Cost Price', style_table_header)
                worksheet.write(6, 6, 'Beginning', style_table_header)
                worksheet.write(6, 7, 'Internal', style_table_header)
                worksheet.write(6, 8, 'Purchase', style_table_header)
                worksheet.write(6, 9, 'Purchase Return', style_table_header)
                worksheet.write(6, 10, 'Sales', style_table_header)
                worksheet.write(6, 11, 'Sales Return', style_table_header)
                worksheet.write(6, 12, 'Adjustment In', style_table_header)
                worksheet.write(6, 13, 'Adjustment Out', style_table_header)
                worksheet.write(6, 14, 'Production In', style_table_header)
                worksheet.write(6, 15, 'Production Out', style_table_header)
                worksheet.write(6, 16, 'Ending', style_table_header)
                worksheet.write(6, 17, 'Valuation', style_table_header)
                prod_row = 7
                prod_col = 0

                get_line = self.get_lines(data)
                for each in get_line:
                    worksheet.write(prod_row, prod_col, each['sku'], style)
                    worksheet.write(prod_row, prod_col+1, each['barcode'], style)
                    worksheet.write(prod_row, prod_col+2, each['name'], style)
                    worksheet.write(prod_row, prod_col+3, each['category'], style)
                    worksheet.write(prod_row, prod_col+4, each['costing_method'], style)
                    worksheet.write(prod_row, prod_col+5, each['cost_price'], style)
                    worksheet.write(prod_row, prod_col+6, each['beginning'], style)
                    worksheet.write(prod_row, prod_col+7, each['internal'], style)
                    # worksheet.write(prod_row, prod_col+8, each['incoming'], style)
                    # worksheet.write(prod_row, prod_col+9, each['sale_value'], style)
                    worksheet.write(prod_row, prod_col+8, each['purchase'], style)
                    worksheet.write(prod_row, prod_col+9, each['purchase_return'], style)
                    worksheet.write(prod_row, prod_col+10, each['sales'], style)
                    worksheet.write(prod_row, prod_col+11, each['sales_return'], style)
                    worksheet.write(prod_row, prod_col+12, each['adjustment_in'], style)
                    worksheet.write(prod_row, prod_col+13, each['adjustment_out'], style)

                    worksheet.write(prod_row, prod_col+14, each['production_in'], style)
                    worksheet.write(prod_row, prod_col+15, each['production_out'], style)

                    worksheet.write(prod_row, prod_col+16, each['net_on_hand'], style)
                    worksheet.write(prod_row, prod_col+17, each['total_value'], style)
                    prod_row = prod_row + 1

                prod_row = 8
                prod_col = 7
            fp = io.BytesIO()
            workbook.save(fp)

            export_id = self.env['sale.day.book.report.excel'].create({'excel_file': base64.encodebytes(fp.getvalue()), 'file_name': filename})
            res = {
                    'view_mode': 'form',
                    'res_id': export_id.id,
                    'res_model': 'sale.day.book.report.excel',
                    'type': 'ir.actions.act_window',
                    'target': 'new'
                }
            return res
        else:
            raise Warning(""" You Don't have xlwt library.\n Please install it by executing this command :  sudo pip3 install xlwt""")


    def action_pivot_report(self):
            report_search = self.env['sale.day.book.pivot.report'].search([])
            if report_search:
                report_search.unlink()
            tree_view_id = self.env.ref('bi_inventory_valuation_reports.pivot_report_wiz_view_tree').id
            data = {'start_date': self.start_date,
                        'end_date': self.end_date, 'warehouse': self.warehouse,
                        'category': self.category,
                        'location_id': self.location_id,
                        'company_id': self.company_id.name,
                        'display_sum': self.display_sum,
                        'currency': self.company_id.currency_id.name,
                        'product_ids': self.product_ids,
                        'filter_by': self.filter_by
                        }
            if self.display_sum:
                ldata = self.get_data(data)
                record = []
                if ldata:
                    for rec in ldata:
                        record.append(rec)
                    if record:
                        for rec in record:
                            _logger.info('===============================%s',rec)
                            r1 = self.env['sale.day.book.pivot.report'].create({
                                # 'name': rec['name'],
                                # 'default_code': rec['sku'],
                                # 'barcode': rec['barcode'],
                                'category': rec['category'],
                                # 'costing_method': rec['costing_method'],
                                'standard_price': rec['cost_price'],
                                'beginning': rec['beginning'],
                                'internal': rec['internal'],
                                'purchase': rec['purchase'],
                                'purchase_return': rec['purchase_return'],
                                'sales': rec['sales'],
                                'sales_return': rec['sales_return'],
                                'adjust_in': rec['adjustment_in'],
                                'adjust_out': rec['adjustment_out'],
                                'prod_in': rec['production_in'],
                                'prod_out': rec['production_out'],
                                'ending': rec['net_on_hand'],
                                'valuation': rec['total_value'],
                            })

                    action = {
                        'type': 'ir.actions.act_window',
                        # 'views': [
                            
                        #     (tree_view_id, 'tree')
                        # ],
                        'view_mode': 'tree',
                        'view_id': self.env.ref('bi_inventory_valuation_reports.pivot_report2_wiz_view_tree').id,
                        'name': ('Pivot Report'),
                        'res_model': 'sale.day.book.pivot.report'
                    }

            else:
                ldata = self.get_lines(data)
                record = []
                if ldata:
                    for rec in ldata:
                        record.append(rec)
                    if record:
                        for rec in record:
                            _logger.info('===============================%s',rec)
                            r1 = self.env['sale.day.book.pivot.report'].create({
                                'name': rec['name'],
                                'default_code': rec['sku'],
                                'barcode': rec['barcode'],
                                'category': rec['category'],
                                'costing_method': rec['costing_method'],
                                'standard_price': rec['cost_price'],
                                'beginning': rec['beginning'],
                                'internal': rec['internal'],
                                'purchase': rec['purchase'],
                                'purchase_return': rec['purchase_return'],
                                'sales': rec['sales'],
                                'sales_return': rec['sales_return'],
                                'adjust_in': rec['adjustment_in'],
                                'adjust_out': rec['adjustment_out'],
                                'prod_in': rec['production_in'],
                                'prod_out': rec['production_out'],
                                'ending': rec['net_on_hand'],
                                'valuation': rec['total_value'],
                            })

                                    

                action = {
                        'type': 'ir.actions.act_window',
                        # 'views': [
                            
                        #     (tree_view_id, 'tree')
                        # ],
                        'view_mode': 'tree',
                        'view_id': self.env.ref('bi_inventory_valuation_reports.pivot_report_wiz_view_tree').id,
                        'name': ('Pivot Report'),
                        'res_model': 'sale.day.book.pivot.report'
                    }
            return action

class sale_day_book_report_excel(models.TransientModel):
    _name = "sale.day.book.report.excel"

    excel_file = fields.Binary('Excel Report For Sale Book Day ')
    file_name = fields.Char('Excel File', size=64)


class sale_day_book_report_pivot(models.Model):
    _name = "sale.day.book.pivot.report"
    

    name = fields.Char(string="Name", readonly=True)
    default_code = fields.Char(string="Default Code", readonly=True)
    barcode = fields.Char(string="Barcode", readonly=True)    
    category = fields.Char(string='Category', readonly=True)
    costing_method = fields.Char(string='Costing Method', readonly=True)
    standard_price = fields.Float(string='Cost Price',readonly=True)
    beginning = fields.Float(string="Beginning",readonly=True)
    internal = fields.Float(string="Internal",readonly=True)
    purchase = fields.Float(string="Purchase",readonly=True)
    purchase_return = fields.Float(string="Purchase Return",readonly=True)
    sales = fields.Float(string="Sales",readonly=True)
    sales_return = fields.Float(string="Sales Return",readonly=True)
    adjust_in = fields.Float(string="Adjustment in",readonly=True)
    adjust_out = fields.Float(string="Adjustment Out",readonly=True)
    prod_in = fields.Float(string="Production In",readonly=True)
    prod_out = fields.Float(string="Production Out",readonly=True)
    ending = fields.Float(string="Ending",readonly=True)
    valuation = fields.Float(string="Valuation",readonly=True)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
