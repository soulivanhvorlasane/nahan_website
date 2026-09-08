# -*- coding: utf-8 -*-
# Part of Nahan.app. See LICENSE file for full copyright and licensing details.

import re
import logging
from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class NahanWebsiteController(http.Controller):

    def _get_localized_seo(self):
        """Retrieve SEO metadata dynamically based on current user language."""
        lang = request.context.get('lang', 'en_US')
        is_lao = 'lo' in lang.lower()

        if is_lao:
            seo_title = "ERP Odoo 18 ລາວ | POS, Website, TaxRIS Integration ສຳລັບ SMEs | Nahan"
            seo_description = (
                "Nahan.app ໃຫ້ບໍລິການ ERP Odoo 18 ສຳລັບ SME ແລະ Startup ໃນລາວ "
                "ພ້ອມ POS, CRM, Accounting, Website ແລະ TaxRIS API Integration."
            )
        else:
            seo_title = "ERP Odoo 18 Laos | SME ERP, POS, Website & TaxRIS Integration | Nahan"
            seo_description = (
                "Nahan.app provides Odoo 18 ERP implementation, POS, CRM, Accounting, "
                "Inventory Management, Website Development, eCommerce, and TaxRIS API Integration "
                "for SMEs and Startups in Laos."
            )

        company = request.env.company
        company_name = company.name or "Nahan.app"
        company_phone = company.phone or "02052746767"
        company_email = company.email or "vorlasanedev@gmail.com"

        addr_parts = [p for p in [company.street, company.street2, company.city, company.state_id.name, company.country_id.name] if p]
        company_address = ', '.join(addr_parts) if addr_parts else "Ban Vansay, Saysettha, Vientiane Capital, Laos"

        return {
            'res_company': company,
            'seo_title': seo_title,
            'seo_description': seo_description,
            'seo_keywords': (
                "ERP Laos, Odoo Laos, ERP Odoo 18, SME ERP Laos, POS Laos, CRM Laos, "
                "Accounting Software Laos, TaxRIS Integration, Website Development Laos, Odoo Partner Laos"
            ),
            'company_name': company_name,
            'company_phone': company_phone,
            'company_email': company_email,
            'company_address': company_address,
        }

    def _extract_number(self, value_str, default=10):
        """Extract first integer digits from a string like '20+' -> 20."""
        if not value_str:
            return default
        match = re.search(r'\d+', str(value_str))
        return int(match.group(0)) if match else default

    @http.route(['/', '/home'], type='http', auth='public', website=True, sitemap=True)
    def index(self, **kwargs):
        """Render the modern corporate homepage for Nahan.app with backend stats."""
        values = self._get_localized_seo()

        # Load backend managed statistics
        stats_record = request.env['nahan.website.stats'].sudo().get_stats()
        values.update({
            'stats': stats_record,
            'projects_target': self._extract_number(stats_record.projects_completed, 20),
            'clients_target': self._extract_number(stats_record.happy_clients, 15),
            'modules_target': self._extract_number(stats_record.odoo_modules, 10),
            'submitted': kwargs.get('submitted') == '1',
            'active_menu': 'home',
        })
        return request.render('nahan_website.homepage', values)

    @http.route('/services', type='http', auth='public', website=True, sitemap=True)
    def services(self, **kwargs):
        """Render the detailed services catalog."""
        values = self._get_localized_seo()
        values.update({
            'page_title': _("Our Services | Odoo 18 ERP & TaxRIS Solutions in Laos | Nahan.app"),
            'page_description': _(
                "Comprehensive ERP implementation, POS retail systems, Lao TaxRIS API integration, "
                "accounting localization, and custom Odoo module development in Laos."
            ),
            'active_menu': 'services',
        })
        return request.render('nahan_website.services_page', values)

    @http.route('/about-us', type='http', auth='public', website=True, sitemap=True)
    def about_us(self, **kwargs):
        """Render the About Us company profile."""
        values = self._get_localized_seo()
        values.update({
            'page_title': _("About Nahan.app | Leading Odoo 18 ERP Specialists in Laos"),
            'page_description': _(
                "Learn about Nahan.app, our mission to empower Lao SMEs and startups with "
                "international-grade Odoo 18 ERP systems, and our certified development team."
            ),
            'active_menu': 'about',
        })
        return request.render('nahan_website.about_page', values)

    @http.route('/blog', type='http', auth='public', website=True, sitemap=True)
    def blog(self, **kwargs):
        """Render the Nahan ERP & Technology Insights Blog."""
        values = self._get_localized_seo()
        values.update({
            'page_title': _("Blog & Insights | Odoo 18 & Lao TaxRIS Guides | Nahan.app"),
            'page_description': _(
                "Read the latest guides and insights on Odoo 18, TaxRIS electronic tax invoice integration, "
                "POS systems, and SME business management in Laos."
            ),
            'active_menu': 'blog',
        })
        return request.render('nahan_website.blog_page', values)

    @http.route(['/contactus', '/contact-us'], type='http', auth='public', website=True, sitemap=True)
    def contact_us(self, **kwargs):
        """Render dedicated Contact Us page with interactive consultation form."""
        values = self._get_localized_seo()
        values.update({
            'page_title': _("Contact Us | Request Free Odoo 18 ERP Consultation | Nahan.app"),
            'page_description': _(
                "Get in touch with Nahan.app in Vientiane, Laos for free consultation, "
                "Odoo 18 demo, and quotation for your SME or Startup."
            ),
            'active_menu': 'contact',
            'submitted': kwargs.get('submitted') == '1',
        })
        return request.render('nahan_website.contact_page', values)

    @http.route('/industries', type='http', auth='public', website=True, sitemap=True)
    def industries(self, **kwargs):
        """Redirect to industries section on homepage."""
        return request.redirect('/#industries')

    @http.route('/api/consultation/submit', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def api_consultation_submit(self, **post):
        """
        JSON endpoint for AJAX consultation form submission.
        Creates a CRM lead in Odoo with sudo permissions.
        """
        data = request.get_json_data() or post
        try:
            lead = self._create_crm_lead(data)
            return {
                'success': True,
                'lead_id': lead.id,
                'message': _("Thank you for your consultation request! Our Odoo 18 specialist will contact you within 24 hours."),
            }
        except Exception as e:
            _logger.exception("Error creating CRM lead from Nahan consultation form: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'message': _("An error occurred while submitting your request. Please call or message us directly via WhatsApp."),
            }

    @http.route('/consultation/submit', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def form_consultation_submit(self, **post):
        """Standard HTTP POST fallback for consultation form submission."""
        try:
            self._create_crm_lead(post)
            redirect_url = post.get('redirect_url', '/?submitted=1#consultation')
            return request.redirect(redirect_url)
        except Exception as e:
            _logger.exception("HTTP POST error creating CRM lead: %s", str(e))
            return request.render('nahan_website.homepage', {
                'error_message': _("Unable to submit request: ") + str(e),
                'active_menu': 'home',
            })

    def _create_crm_lead(self, data):
        """Helper to create a crm.lead record with detailed consultation info."""
        company_name = (data.get('company_name') or '').strip()
        contact_name = (data.get('contact_name') or '').strip()
        phone = (data.get('phone') or '').strip()
        email = (data.get('email') or '').strip()
        business_type = (data.get('business_type') or '').strip()
        employee_count = (data.get('employee_count') or '').strip()
        notes = (data.get('message') or data.get('notes') or '').strip()

        # Handle interested services
        services = data.get('interested_services', [])
        if isinstance(services, str):
            services_list = [s.strip() for s in services.split(',') if s.strip()]
        elif isinstance(services, list):
            services_list = [str(s).strip() for s in services if s]
        else:
            services_list = []
        services_str = ', '.join(services_list) if services_list else _("General Odoo 18 Consultation")

        # Validation
        if not contact_name and not company_name:
            raise ValueError(_("Please provide your contact name or company name."))
        if not phone and not email:
            raise ValueError(_("Please provide a phone number or email address so we can reach you."))

        # Build lead name
        display_title = company_name or contact_name
        lead_name = f"[Nahan ERP] {display_title} - {services_str[:40]}"

        # Compose rich HTML description
        lang_code = request.context.get('lang', 'en_US')
        lang_label = "Lao (ພາສາລາວ)" if 'lo' in lang_code else "English"

        description_html = f"""
        <div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">
            <h3 style="color: #0A2540; border-bottom: 2px solid #4F46E5; padding-bottom: 6px;">
                🚀 Nahan.app Website Consultation Inquiry
            </h3>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                <tr><td style="padding: 6px; font-weight: bold; width: 180px; color: #4F46E5;">Company:</td><td style="padding: 6px;">{company_name or 'N/A'}</td></tr>
                <tr style="background-color: #F8FAFC;"><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Contact Person:</td><td style="padding: 6px;">{contact_name or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Phone:</td><td style="padding: 6px;">{phone or 'N/A'}</td></tr>
                <tr style="background-color: #F8FAFC;"><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Email:</td><td style="padding: 6px;">{email or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Industry / Sector:</td><td style="padding: 6px;">{business_type or 'Not specified'}</td></tr>
                <tr style="background-color: #F8FAFC;"><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Company Size:</td><td style="padding: 6px;">{employee_count or 'Not specified'}</td></tr>
                <tr><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Interested Services:</td><td style="padding: 6px; font-weight: 600; color: #06B6D4;">{services_str}</td></tr>
                <tr style="background-color: #F8FAFC;"><td style="padding: 6px; font-weight: bold; color: #4F46E5;">Website Language:</td><td style="padding: 6px;">{lang_label} ({lang_code})</td></tr>
            </table>
            <div style="margin-top: 15px; padding: 12px; background: #EEF2FF; border-left: 4px solid #4F46E5; border-radius: 4px;">
                <strong>Client Message / Requirements:</strong><br/>
                <p style="margin: 6px 0 0 0; white-space: pre-wrap;">{notes or 'No specific message provided.'}</p>
            </div>
            <p style="margin-top: 12px; font-size: 11px; color: #94A3B8;">
                Generated automatically by Nahan.app website consultation module on {fields_date()}
            </p>
        </div>
        """

        # Locate or create CRM tags
        crm_tag_obj = request.env['crm.tag'].sudo()
        tag_ids = []
        for tag_name in ['Website Lead', 'Nahan Consultation']:
            tag = crm_tag_obj.search([('name', '=', tag_name)], limit=1)
            if not tag:
                tag = crm_tag_obj.create({'name': tag_name})
            tag_ids.append(tag.id)

        if 'TaxRIS' in services_str:
            taxris_tag = crm_tag_obj.search([('name', '=', 'TaxRIS Inquiry')], limit=1)
            if not taxris_tag:
                taxris_tag = crm_tag_obj.create({'name': 'TaxRIS Inquiry'})
            tag_ids.append(taxris_tag.id)

        lead_vals = {
            'name': lead_name,
            'partner_name': company_name,
            'contact_name': contact_name,
            'phone': phone,
            'email_from': email,
            'description': description_html,
            'type': 'lead',
            'priority': '2',
            'tag_ids': [(6, 0, tag_ids)],
            'is_nahan_consultation': True,
        }

        crm_fields = request.env['crm.lead']._fields
        if 'business_type' in crm_fields and business_type:
            lead_vals['business_type'] = business_type
        if 'employee_count' in crm_fields and employee_count:
            lead_vals['employee_count'] = employee_count
        if 'interested_services' in crm_fields and services_str:
            lead_vals['interested_services'] = services_str

        return request.env['crm.lead'].sudo().create(lead_vals)


def fields_date():
    from datetime import datetime
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
