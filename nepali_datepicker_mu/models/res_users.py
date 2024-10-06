from odoo import models, fields, api


class res_users(models.Model):
	_inherit = 'res.users'
	
	@api.model
	def datepicker_localization(self):
		user_brow_obj = self.env['res.users'].search([('id','=',self._uid)])
		res_lang_obj = self.env['res.lang']
		lang_ids = res_lang_obj.search([('code', '=', user_brow_obj.lang)])
		date_format = '%m/%d/%Y'
		lang = 'en'
		if lang_ids:
			langs = res_lang_obj.search([('id','=',lang_ids[0].id)]).code
			lang = langs[:2]
			date_format = res_lang_obj.search([('id','=',lang_ids[0].id)]).date_format
			print(lang)
			print (date_format)
		return {
			'lang': str(lang) or '',
			'date_format': date_format
		}