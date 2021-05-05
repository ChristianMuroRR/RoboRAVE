# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import werkzeug
from werkzeug.exceptions import Forbidden, NotFound
from odoo.http import request, route
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.website_event.controllers.main import WebsiteEventController
# from odoo.addons.website.controllers.main import Website
# from odoo.addons.website_form.controllers.main import WebsiteForm

# VALUES EXTRA IN ATTENDENCE
class WebsiteEventController(WebsiteEventController):

    def _process_tickets_form(self, event, form_details):
        """ Process posted data about ticket order. Generic ticket are supported
        for event without tickets (generic registration).

        :return: list of order per ticket: [{
            'id': if of ticket if any (0 if no ticket),
            'ticket': browse record of ticket if any (None if no ticket),
            'name': ticket name (or generic 'Registration' name if no ticket),
            'quantity': number of registrations for that ticket,
        }, {...}]
        """
        ticket_order = {}
        for key, value in form_details.items():
            registration_items = key.split('nb_register-')
            if len(registration_items) != 2:
                continue
            ticket_order[int(registration_items[1])] = int(value)

        ticket_dict = dict((ticket.id, ticket) for ticket in request.env['event.event.ticket'].search([
            ('id', 'in', [tid for tid in ticket_order.keys() if tid]),
            ('event_id', '=', event.id)
        ]))
        return [{
            'id': tid if ticket_dict.get(tid) else 0,
            'ticket': ticket_dict.get(tid),
            'name': ticket_dict[tid]['name'] if ticket_dict.get(tid) else _('Registration'),
            'quantity': count,
        } for tid, count in ticket_order.items() if count]


    @http.route(['/event/<model("event.event"):event>/registration/new'], type='json', auth="public", methods=['POST'], website=True)
    def registration_new(self, event, **post):
        # if not event.can_access_from_current_website():
        #     raise werkzeug.exceptions.NotFound()
        division_rec = request.env['res.partner.age.division'].sudo().search([])
        tickets = self._process_tickets_form(event, post)
        availability_check = True
        if event.seats_limited:
            ordered_seats = 0
            for ticket in tickets:
                ordered_seats += ticket['quantity']
            if event.seats_available < ordered_seats:
                availability_check = False
        if not tickets:
            return False
        return request.env['ir.ui.view']._render_template("website_event.registration_attendee_details", {'tickets': tickets, 'division_rec': division_rec, 'event': event, 'availability_check': availability_check})

    def _process_attendees_form(self, event, form_details):
        """ Process data posted from the attendee details form.

        :param form_details: posted data from frontend registration form, like
            {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
        """

        # allowed_fields = {'name', 'phone', 'email', 'mobile', 'event_id', 'partner_id', 'event_ticket_id', 'division_id', 'team_id'}
        allowed_fields = {'name', 'phone', 'email', 'mobile', 'event_id', 'partner_id', 'event_ticket_id', 'division_id', 'players'}
        registration_fields = {key: v for key, v in request.env['event.registration']._fields.items() if key in allowed_fields}
        registrations = {}
        global_values = {}
        for key, value in form_details.items():
            counter, attr_name = key.split('-', 1)
            field_name = attr_name.split('-')[0]
            if field_name not in registration_fields:
                continue
            elif isinstance(registration_fields[field_name], (fields.Many2one, fields.Integer)):
                value = int(value) or False  # 0 is considered as a void many2one aka False
            else:
                value = value

            if counter == '0':
                global_values[attr_name] = value
            else:
                registrations.setdefault(counter, dict())[attr_name] = value
        for key, value in global_values.items():
            for registration in registrations.values():
                registration[key] = value

        return list(registrations.values())