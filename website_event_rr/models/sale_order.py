# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _website_product_id_change(self, order_id, product_id, qty=0):
        # print('enter _website_product_id_change')
        # registration = self.env['event.registration'].search([("sale_order_id", "=", order_id)])
        # print('/1',registration.ids)

        order = self.env['sale.order'].sudo().browse(order_id)

        if self._context.get('pricelist') != order.pricelist_id.id:
            self = self.with_context(pricelist=order.pricelist_id.id)
        values = super(SaleOrder, self)._website_product_id_change(order_id, product_id, qty=qty)
        event_ticket_id = None

        if self.env.context.get("event_ticket_id"):
            event_ticket_id = self.env.context.get("event_ticket_id")
        else:
            product = self.env['product.product'].browse(product_id)

            if product.event_ticket_ids:
                event_ticket_id = product.event_ticket_ids[0].id
        if event_ticket_id:
            ticket = self.env['event.event.ticket'].browse(event_ticket_id)

            if product_id != ticket.product_id.id:
                raise UserError(_("The ticket doesn't match with this product."))
            values['product_id'] = ticket.product_id.id
            values['event_id'] = ticket.event_id.id
            values['event_ticket_id'] = ticket.id

            if order.pricelist_id.discount_policy == 'without_discount':
                values['price_unit'] = ticket.price
            else:
                values['price_unit'] = ticket.price_reduce
            values['name'] = ticket._get_ticket_multiline_description()
        # avoid writing related values that end up locking the product record
        values.pop('event_ok', None)
        return values
    


