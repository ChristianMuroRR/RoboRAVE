# -*- coding: utf-8 -*-
# details
import logging
from odoo.http import request
from odoo.exceptions import UserError
from odoo.addons.web.controllers.main import ensure_db, Home


_logger = logging.getLogger(__name__)

class AuthSignupHome(Home):

	def get_auth_signup_qcontext(self):
		qcontext = super(AuthSignupHome, self).get_auth_signup_qcontext()
		qcontext['countries'] = request.env["res.country"].sudo().search([])
		return qcontext

	def do_signup(self, qcontext):
		""" Shared helper that creates a res.partner out of a token """
		values = { key: qcontext.get(key) for key in ('login', 'name', 'password', 'last_name', 'country_id', 'birth_month', 'birth_year', 'type_user', 'gender') }
		if not values:
			raise UserError(_("The form was not properly filled in."))
		if values.get('password') != qcontext.get('confirm_password'):
			raise UserError(_("Passwords do not match; please retype them."))
		supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
		lang = request.context.get('lang', '').split('_')[0]
		if lang in supported_lang_codes:
			values['lang'] = lang
		self._signup_with_values(qcontext.get('token'), values)
		request.env.cr.commit()