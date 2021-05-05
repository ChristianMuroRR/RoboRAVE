from odoo import api, fields, models, _

class EventTicket(models.Model):
    _inherit = 'event.event.ticket'

    division_ids = fields.Many2many('res.partner.age.division', string='Divisions')