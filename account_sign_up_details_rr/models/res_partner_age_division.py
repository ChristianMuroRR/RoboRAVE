# Copyright 2019-2020: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerDateDivision(models.Model):
    _name = "res.partner.age.division"
    _description = "Partner Age Division"

    def _default_age_from(self):
        age_from = 0
        last_age_division = self.env["res.partner.age.division"].search(
            [], order="age_to desc", limit=1
        )
        if last_age_division:
            age_from = last_age_division.age_to + 1
        return age_from

    name = fields.Char(string="Name", required=True)
    age_from = fields.Integer(
        string="From", required=True, default=lambda self: self._default_age_from()
    )
    age_to = fields.Integer(string="To", required=True)

    _sql_constraints = [("name_uniq", "unique (name)", "A name must be unique !")]

    @api.constrains("age_from", "age_to")
    def _validate_division(self):
        for rec in self:
            if rec.age_from >= rec.age_to:
                raise ValidationError(
                    _("%s is not a valid division (%s >= %s)")
                    % (rec.name, rec.age_from, rec.age_to)
                )
            division_id = rec.search(
                [
                    ("age_from", "<=", rec.age_to),
                    ("age_to", ">=", rec.age_from),
                    ("id", "!=", rec.id),
                ],
                limit=1,
            )
            if division_id:
                raise ValidationError(
                    _("%s is overalapping with division %s") % (rec.name, division_id.name)
                )
