# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random

from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied, AccessError
from odoo.tools import html_escape

class TeamTeam(models.Model):
    _name = "team.team"
    _description = 'Teams'

    name = fields.Char('Name')
    contact_name = fields.Char('Contact Name')
    title = fields.Char('Title')
    number = fields.Char('Number')
    description = fields.Text('Description')
    priority = fields.Integer('Priority')
    partner_name = fields.Char('Partner Name')
    phone = fields.Char('Phone')
    mobile = fields.Char('Mobile')
    email_from = fields.Char('Email From', help="Email address of the sender. This field is set when no matching partner is found and replaces the author_id field in the chatter.")
    date_deadline = fields.Date('Expected Closing', readonly=True)
    stage_id = fields.Many2one('team.stage', string='Stage', index=True, tracking=True, readonly=False, store=True, copy=False, ondelete='restrict')
    member_1_id = fields.Many2one('res.partner', 'Member #1', tracking=True, help="Partner this case has been forwarded/assigned to.", index=True)
    user_ids = fields.Many2many('res.users', string='Users of Team')

    user_1_id = fields.Many2one('res.users', string='User 1')
    user_2_id = fields.Many2one('res.users', string='User 2')
    user_3_id = fields.Many2one('res.users', string='User 3')
    user_4_id = fields.Many2one('res.users', string='User 4')
    players = fields.Integer('Players')
    division_id = fields.Many2one('res.partner.age.division', string='Division')

    partner_assigned_id = fields.Many2one('res.partner', 'Assigned Partner', tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="Partner this case has been forwarded/assigned to.", index=True)

    def update_team_portal(self, values, **kwargs):
        print('enter update_team_portal')
        self.check_access_rights('write')
        # values['user_ids'] = self._user_to_write_vals(kwargs.get('post_users', ''))
        # user_ids = False
        if 'post_users' in values:
            values = set(self.new({'user_ids': values['post_users']}).user_ids.ids)
        # print('values of user_ids',user_ids)
        # users_ids = set(self.new({'user_ids': values['post_users']}).ids)
        # sale_orders = self.new({'sale_order_ids': values['sale_order_ids']}).sale_order_ids
        # values['user_ids'] = self._user_to_write_vals(kwargs.get('post_users', ''))
        #
        users = [values['post_user_1'],
                values['post_user_2'],
                values['post_user_3'],
                values['post_user_4']]

        print('values of update_team_portal',users)
        for team in self:
            team_values = {
                'name': values['name'],
                'user_ids': users,
                              # values['users'],
            }
            team.write(team_values)

    @api.model
    def create_team_portal(self, values):
        # if not (self.env.user.partner_id.grade_id or self.env.user.commercial_partner_id.grade_id):
        #     raise AccessDenied()
        user = self.env.user
        self = self.sudo()
        # if not (values['contact_name'] and values['description'] and values['title']):
        #     return {
        #         'errors': _('All fields are required !')
        #     }
        # tag_own = self.env.ref('website_teams.tag_portal_lead_own_opp', False)
        values = {
            # 'contact_name': values['contact_name'],
            'name': values['title'],

            # 'description': values['description'],
            'priority': '2',
            'partner_assigned_id': user.commercial_partner_id.id,
        }
        # if tag_own:
        #     values['tag_ids'] = [(4, tag_own.id, False)]

        team = self.create(values)
        # team.assign_salesman_of_assigned_partner()
        # team.convert_opportunity(team.partner_id.id)
        return {
            'id': team.id
        }

    @api.model
    def _user_to_write_vals(self, tags=''):
        User = self.env['res.users']
        post_users = []
        existing_keep = [21]
        user = self.env.user

        for tag in (tag for tag in tags.split(',') if tag):
            if tag.startswith('_'):  # it's a new tag
                # check that not already created meanwhile or maybe excluded by the limit on the search
                users_ids = User.search([('name', '=', tag[1:])])
                if users_ids:
                    existing_keep.append(int(users_ids[0]))
                else:
                    # check if user have Karma needed to create need tag
                    if user.exists() and user.karma >= self.karma_tag_create and len(tag) and len(tag[1:].strip()):
                        post_users.append((0, 0, {'name': tag[1:], 'forum_id': self.id}))
            else:
                existing_keep.append(int(tag))
        post_users.insert(0, [6, 0, existing_keep])

        return post_users