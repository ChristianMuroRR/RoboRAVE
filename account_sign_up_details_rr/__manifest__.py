# -*- coding: utf-8 -*-
{
  "name"                 :  "Website RoboRAVE On Signup Form",
  "summary"              :  """Add a extra fields for users to share their data during the sign up.""",
  "category"             :  "Website",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "license"              :  "Other proprietary",
  "description"          :  """Website RoboRAVE On Signup Form""",
  "depends"              :  ['auth_signup','contacts','portal'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'data/age_division_cron.xml',
                             'views/res_partner_view.xml',
                             'views/account_details_template.xml',
                             'views/portal_templates.xml',
                             'views/res_partner_age_division_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
