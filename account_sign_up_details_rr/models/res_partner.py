# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _

class ResPartner(models.Model):
	_inherit = 'res.partner'
	# _sql_constraints = [
    #     ('birth_year_rage', 'check(birth_year >= 1921 and birth_year <= 2020)', 'Birth Year should be between 1921 to 2020'),
    # ]


	last_name = fields.Char( string='Last Name')
	birth_month = fields.Selection([
        ('01', 'January'),('02', 'February'),('03', 'March'),('04', 'April'),('05', 'May'),('06', 'June'),('07', 'July'),('08', 'August'),
		('09', 'September'),('10', 'October'),('11', 'November'),('12', 'December')], default="", help="Birth Month")
	birth_year = fields.Integer( string='Year of Birth')
	age = fields.Integer(readonly=True, compute='_compute_age', string='Age')
	type_user = fields.Selection([
        ('coach', 'Coach'),
        ('player', 'Player')], default="player", required=True,
        help="Use 'Coach' to create teams. Use 'Player' to play. Use 'Indefinite' to configure later")
	gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")])
	age_division_id = fields.Many2one("res.partner.age.division", "Age Division", compute="_compute_age_division_id", store=True,)

	@api.depends("birth_year")
	def _compute_age(self):
		for record in self:
			age = 0
			if record.birth_year:
				actual_year = fields.Date.today().year
				age = actual_year - record.birth_year
			record.age = age

	@api.depends("age")
	def _compute_age_division_id(self):
		age_divisions = self.env["res.partner.age.division"].search([])
		for record in self:
			if not record.age:
				age_division = False
			else:
				age_division = (
                    age_divisions.filtered(
                        lambda age_division: age_division.age_from
                        <= record.age
                        <= age_division.age_to
                    )
                    or False
                )
		if record.age_division_id != age_division:
			record.age_division_id = age_division and age_division.id or age_division

	@api.model
	def _cron_update_age_division_id(self):
		"""
        This method is called from a cron job.
        It is used to update age division on contact
        """
		partners = self.search([("birth_year", "!=", False)])
		partners._compute_age_division_id()