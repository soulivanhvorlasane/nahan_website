# -*- coding: utf-8 -*-
# Part of Nahan.app. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_nahan_consultation = fields.Boolean(
        string="Nahan Website Consultation",
        default=False,
        index=True,
        help="Flagged if generated from Nahan.app website consultation form.",
    )
    business_type = fields.Selection(
        selection=[
            ('retail', 'Retail / Supermarket'),
            ('wholesale', 'Wholesale & Distribution'),
            ('manufacturing', 'Manufacturing / Factory'),
            ('services', 'Services & Consulting'),
            ('hospitality', 'Hospitality / Restaurant / Hotel'),
            ('construction', 'Construction & Real Estate'),
            ('education', 'Education & Training'),
            ('healthcare', 'Healthcare & Pharmacy'),
            ('logistics', 'Logistics & Transportation'),
            ('other', 'Other / Startup'),
        ],
        string="Business Type",
        help="Type of industry or business sector.",
    )
    employee_count = fields.Selection(
        selection=[
            ('1-10', '1 - 10 Employees'),
            ('11-50', '11 - 50 Employees'),
            ('51-200', '51 - 200 Employees'),
            ('200+', '200+ Employees'),
        ],
        string="Company Size",
        help="Number of employees in the organization.",
    )
    interested_services = fields.Char(
        string="Interested Services",
        help="Comma-separated list of services or modules requested.",
    )
