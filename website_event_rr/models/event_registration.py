from odoo import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    division_id = fields.Many2one('res.partner.age.division', string='Division')
    players = fields.Integer(string='Players')
    team_created = fields.Boolean(string='Team Create', compute='_create_team',store=True, readonly=False)

    @api.depends('state')
    def _create_team(self):
        for record in self:
            if record.state == 'open':
                temp = record
                for val in temp:
                    vals = {
                    'name': val.name,
                    'partner_assigned_id': val.partner_id.id,
                    'players': val.players,
                    'division_id': val.division_id.id
                }
                record.team_created = True
                self.env['team.team'].create(vals)
                print('Ok')
                    # registration.date_closed = fields.Datetime.now()
            else:
                record.team_created = False    # registration.date_closed = False
                print('No Ok')