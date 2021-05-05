# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import datetime
import werkzeug.urls

from collections import OrderedDict
from werkzeug.exceptions import NotFound

from odoo import fields
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_partner.controllers.main import WebsitePartnerPage

from odoo.tools.translate import _


class WebsiteAccount(CustomerPortal):

    @http.route('/team/get_users', type='http', auth="public", methods=['GET'], website=True, sitemap=False)
    def user_read(self, query='', limit=25, **post):
        data = request.env['res.users'].search_read(
            domain=[('name', '=ilike', (query or '') + "%")],
            fields=['id', 'name'],
            limit=int(limit),
        )
        return json.dumps(data)

    def get_domain_my_team(self, user):
        return [
            ('partner_assigned_id', '=', request.env.user.commercial_partner_id.id)
        ]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'team_count' in counters:
            values['team_count'] = request.env['team.team'].search_count(self.get_domain_my_team(request.env.user))
        return values

    @http.route(['/my/teams', '/my/teams/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_teams(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        TeamTeam = request.env['team.team']
        domain = self.get_domain_my_team(request.env.user)
        today = fields.Date.today()
        this_week_end_date = fields.Date.to_string(fields.Date.from_string(today) + datetime.timedelta(days=7))
        searchbar_filters = {
            'all': {'label': _('Active'), 'domain': []},
            'today': {'label': _('Today Activities'), 'domain': [('activity_date_deadline', '=', today)]},
            'week': {'label': _('This Week Activities'),
                     'domain': [('activity_date_deadline', '>=', today), ('activity_date_deadline', '<=', this_week_end_date)]},
            'overdue': {'label': _('Overdue Activities'), 'domain': [('activity_date_deadline', '<', today)]},
            'won': {'label': _('Won'), 'domain': [('stage_id.is_won', '=', True)]},
            'lost': {'label': _('Lost'), 'domain': [('active', '=', False), ('probability', '=', 0)]},
        }
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'contact_name': {'label': _('Contact Name'), 'order': 'contact_name'},
            'revenue': {'label': _('Expected Revenue'), 'order': 'expected_revenue desc'},
            'probability': {'label': _('Probability'), 'order': 'probability desc'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
        }
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        if filterby == 'lost':
            TeamTeam = TeamTeam.with_context(active_test=False)

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        # pager
        team_count = TeamTeam.search_count(domain)
        pager = request.website.pager(
            url="/my/teams",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=team_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager
        teams = TeamTeam.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'teams': teams,
            'page_name': 'team',
            'default_url': '/my/teams',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("website_teams.portal_my_teams", values)

    @http.route(['''/my/team/<model('team.team'):team>'''], type='http', auth="user", website=True)
    def portal_my_team(self, team, **kw):
        return request.render(
            "website_teams.portal_my_team", {
                'team': team,
                'members': request.env['res.partner'].sudo().search([]),
                'users': request.env['res.users'].sudo().search([]),
                # 'user_activity': team.sudo().activity_ids.filtered(lambda activity: activity.user_id == request.env.user)[:1],
                'stages': request.env['team.stage'].search([], order='sequence desc, name desc, id desc'),
                # 'stages': request.env['team.stage'].search([('is_won', '!=', True)], order='sequence desc, name desc, id desc'),
                'activity_types': request.env['mail.activity.type'].sudo().search([]),
                'states': request.env['res.country.state'].sudo().search([]),
                'countries': request.env['res.country'].sudo().search([]),
            })