# -*- coding: utf-8 -*-
# Part of Nahan.app. See LICENSE file for full copyright and licensing details.

{
    'name': 'Nahan.app - ERP Odoo 18 Solutions for Laos',
    'version': '18.0.1.0.0',
    'category': 'Website/Theme',
    'summary': 'Corporate website for Nahan.app - ERP Odoo 18 consulting, POS, Lao TaxRIS API integration, and CRM lead generation.',
    'description': """
Nahan.app Corporate Website - Odoo 18
=====================================
A modern, responsive corporate website built specifically for **Nahan.app**, an ERP Odoo consulting firm in Laos.

Key Features:
-------------
* **Modern SaaS UI**: Built with Bootstrap 5, high-conversion layout, and enterprise slate & indigo styling.
* **10 Homepage Sections**: Hero banner, Service catalog, Why Choose Nahan, Odoo Modules grid, Industries served, Consultation form, Customer journey roadmap, FAQ accordion, CTA banner, and Corporate footer.
* **Automated CRM Lead Generation**: Secure AJAX consultation form creates structured `crm.lead` records with contact details, company size, business sector, and selected modules.
* **Lao TaxRIS API Integration Showcase**: Highlights official compliance with the Lao Tax Department's electronic tax invoicing system.
* **Bilingual Support (English & Lao)**: Multi-language support with official locales `en_US` and `lo_LA`, clean URL prefixes, and gettext catalogs (`lo.po`, `en.po`, `nahan_website.pot`).
* **Subpages Included**: Dedicated `/services`, `/about-us`, and `/contact-us` pages.
* **Technical SEO & Schema.org**: JSON-LD structured data for `ProfessionalService` / `LocalBusiness`, Open Graph tags, and Twitter Cards.
* **Lao SME Optimizations**: Dynamic animated statistics counter, direct WhatsApp chat floating widget, and mobile-first responsiveness.
    """,
    'author': 'Nahan.app',
    'website': 'https://nahan.app',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'website_sale',
        'website_crm',
        'crm',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stats_views.xml',
        'views/website_templates.xml',
        'views/page_templates.xml',
        'views/menu.xml',
        'data/website_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'nahan_website/static/src/scss/style.scss',
            'nahan_website/static/src/js/main.js',
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
