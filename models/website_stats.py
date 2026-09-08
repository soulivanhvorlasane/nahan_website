# -*- coding: utf-8 -*-
# Part of Nahan.app. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class NahanWebsiteStats(models.Model):
    _name = 'nahan.website.stats'
    _description = 'Nahan Website Statistics'

    name = fields.Char(
        string="Configuration Name",
        default="Nahan.app Website Statistics",
        required=True,
    )
    projects_completed = fields.Char(
        string="Projects Completed",
        default="20+",
        required=True,
        help="Display count for completed ERP/POS implementations (e.g. 20+)",
    )
    happy_clients = fields.Char(
        string="Happy Clients",
        default="15+",
        required=True,
        help="Display count for satisfied SME/startup clients in Laos (e.g. 15+)",
    )
    odoo_modules = fields.Char(
        string="Odoo Modules",
        default="10+",
        required=True,
        help="Number of core Odoo 18 business applications deployed (e.g. 10+)",
    )
    support_hours = fields.Char(
        string="Support Availability",
        default="24/7",
        required=True,
        help="Support availability guarantee for Lao clients (e.g. 24/7 or 99.9%)",
    )
    active = fields.Boolean(default=True)

    @api.model
    def get_stats(self):
        """Retrieve active stats record or initialize with default values."""
        stats = self.search([('active', '=', True)], limit=1)
        if not stats:
            stats = self.create({
                'name': 'Nahan.app Default Statistics',
                'projects_completed': '20+',
                'happy_clients': '15+',
                'odoo_modules': '10+',
                'support_hours': '24/7',
            })
        return stats

    @api.model
    @api.model
    def cleanup_duplicate_menus(self):
        """
        Aggressively search and purge duplicate/unwanted menu items across all websites.
        Ensures exactly ONE instance of each required menu in the exact SaaS order:
        - Home (10)
        - Services (20)
        - ERP Solutions (30)
        - API Integration (40)
        - Blog (50)
        - About Us (60)
        - Contact Us (70)

        Completely removes Shop, Jobs, Products, Careers menus.
        Syncs company logo to website logo.
        """
        _logger.info("Purging unwanted/duplicate website menus and configuring clean Nahan SaaS navigation...")
        menu_obj = self.env['website.menu'].sudo()

        # 1. Purge unwanted default menus completely (Shop, Jobs, Products, Careers)
        for xml_id in ['website_sale.menu_shop', 'website_hr_recruitment.menu_jobs']:
            menu_rec = self.env.ref(xml_id, raise_if_not_found=False)
            if menu_rec:
                try:
                    menu_rec.unlink()
                except Exception:
                    try:
                        menu_rec.write({'active': False})
                    except Exception:
                        pass

        unwanted_menus = menu_obj.search([
            '|', '|', '|', '|', '|', '|',
            ('url', 'in', ['/shop', '/jobs', '/careers', '/products']),
            ('url', '=ilike', '/shop%'),
            ('url', '=ilike', '/jobs%'),
            ('name', '=ilike', 'Shop'),
            ('name', '=ilike', 'Jobs'),
            ('name', '=ilike', 'Careers'),
            ('name', '=ilike', 'Products'),
        ])
        for unw in unwanted_menus:
            try:
                _logger.info("Purging unwanted menu %s (%s, %s)", unw.id, unw.name, unw.url)
                unw.unlink()
            except Exception as e:
                _logger.warning("Could not unlink unwanted menu %s: %s", unw.id, e)

        # Also purge Odoo 18 and Industries menus from navigation
        purge_menus = menu_obj.search([
            '|', '|', '|', '|', '|',
            ('url', 'in', ['/#industries', '/industries', '#industries', '/services#odoo18', '/odoo-18', '/odoo18', '#odoo18', '/#odoo18']),
            ('name', '=ilike', 'Industries'),
            ('name', '=ilike', 'Our Industries'),
            ('name', '=ilike', 'Odoo 18'),
            ('name', '=ilike', 'Odoo 18 ERP'),
            ('name', '=ilike', 'Odoo'),
        ])
        for pm in purge_menus:
            try:
                _logger.info("Purging menu %s (%s, %s)", pm.id, pm.name, pm.url)
                pm.unlink()
            except Exception as e:
                _logger.warning("Could not unlink menu %s: %s", pm.id, e)

        # 2. Sync company logo with website logo so "YourLogo" placeholder is eliminated
        websites = self.env['website'].sudo().search([])
        for site in websites:
            if site.company_id and site.company_id.logo:
                try:
                    site.logo = site.company_id.logo
                except Exception as e:
                    _logger.warning("Could not sync company logo to website %s: %s", site.id, e)

        menu_specs = [
            {
                'xml_id': 'nahan_website.menu_services',
                'name': 'Services',
                'names': ['Services', 'services', 'Our Services', 'our services'],
                'url': '/services',
                'urls': ['/services', '/our-services', '/services/'],
                'sequence': 20,
            },
            {
                'xml_id': 'nahan_website.menu_erp_solutions',
                'name': 'ERP Solutions',
                'names': ['ERP Solutions', 'erp solutions', 'ERP Solution', 'erp solution', 'ERP', 'erp'],
                'url': '/services#erp',
                'urls': ['/services#erp', '/erp-solutions', '/erp', '#erp', '#erp-solutions', '/#erp', '/services#erp-solutions'],
                'sequence': 10,
                'parent_xml_id': 'nahan_website.menu_services',
            },
            {
                'xml_id': 'nahan_website.menu_taxris_integration',
                'name': 'API Integration',
                'names': ['API Integration', 'api integration', 'TaxRIS Integration', 'taxris integration', 'TaxRIS', 'taxris', 'TaxRIS API', 'Taxris', 'API', 'api'],
                'url': '/services#api',
                'urls': ['/services#api', '/services#taxris', '/taxris-integration', '/api-integration', '/taxris', '#taxris', '/#taxris', '#api'],
                'sequence': 20,
                'parent_xml_id': 'nahan_website.menu_services',
            },
            {
                'xml_id': 'nahan_website.menu_blog',
                'name': 'Blog',
                'names': ['Blog', 'blog', 'Insights', 'insights', 'News', 'news'],
                'url': '/blog',
                'urls': ['/blog', '/news', '/insights', '/blog/'],
                'sequence': 30,
            },
            {
                'xml_id': 'nahan_website.menu_about',
                'name': 'About Us',
                'names': ['About Us', 'about us', 'About', 'about', 'About us'],
                'url': '/about-us',
                'urls': ['/about-us', '/about', '/aboutus', '/about-us/'],
                'sequence': 40,
            },
            {
                'xml_id': 'nahan_website.menu_contact',
                'name': 'Contact Us',
                'names': ['Contact Us', 'contact us', 'Contact', 'contact', 'Contact us', 'Get in Touch'],
                'url': '/contactus',
                'urls': ['/contactus', '/contact-us', '/contact', '/contact-us/'],
                'sequence': 50,
            },
        ]

        main_menu = self.env.ref('website.main_menu', raise_if_not_found=False)
        if not main_menu:
            first_website = self.env['website'].sudo().search([], limit=1)
            main_menu = first_website.menu_id if first_website else None

        # 3. Deduplicate Home menu: url in ['/', '/home', '', '#'] and name matching Home
        home_menus = menu_obj.search([
            '|', '|', '|',
            ('url', 'in', ['/', '/home', '', '#']),
            ('name', '=ilike', 'Home'),
            ('name', '=ilike', 'Homepage'),
            ('name', '=ilike', 'ໜ້າຫຼັກ'),
        ], order='id asc')

        if len(home_menus) > 1:
            _logger.info("Found %d Home menus. Keeping primary (ID: %s) and unlinking %d duplicates.",
                         len(home_menus), home_menus[0].id, len(home_menus) - 1)
            vals = {'name': 'Home', 'url': '/', 'sequence': 10}
            if main_menu:
                vals['parent_id'] = main_menu.id
            home_menus[0].write(vals)
            for dup in home_menus[1:]:
                try:
                    dup.unlink()
                except Exception as e:
                    _logger.warning("Could not unlink duplicate Home menu %s: %s", dup.id, e)
        elif home_menus:
            vals = {'name': 'Home', 'url': '/', 'sequence': 10}
            if main_menu:
                vals['parent_id'] = main_menu.id
            home_menus[0].write(vals)

        # 4. Deduplicate each required menu item across the entire database
        for spec in menu_specs:
            target_record = None
            if spec.get('xml_id'):
                target_record = self.env.ref(spec['xml_id'], raise_if_not_found=False)

            # Search all matching records in DB by URL or Name (with case-insensitive pattern matching)
            search_domain = [
                '|', '|', '|',
                ('url', 'in', spec['urls']),
                ('url', '=ilike', spec['url']),
                ('name', 'in', spec['names']),
                ('name', '=ilike', spec['name']),
            ]

            # For Odoo 18 and ERP Solutions, also match broader ilike if specified
            if 'Odoo 18' in spec['name']:
                search_domain = ['|', ('name', 'ilike', 'Odoo 18')] + search_domain
            elif 'ERP' in spec['name']:
                search_domain = ['|', ('name', 'ilike', 'ERP Solution')] + search_domain

            all_matches = menu_obj.search(search_domain, order='id asc')

            if not all_matches:
                continue

            # If target_record exists and is among matches, keep it. Otherwise keep the first match.
            if target_record and target_record.id in all_matches.ids:
                keeper = target_record
            else:
                keeper = all_matches[0]

            keeper_vals = {
                'name': spec['name'],
                'url': spec['url'],
                'sequence': spec['sequence'],
            }
            if spec.get('parent_xml_id'):
                parent_menu = self.env.ref(spec['parent_xml_id'], raise_if_not_found=False)
                if not parent_menu:
                    parent_menu = menu_obj.search([('url', '=', '/services'), ('name', '=ilike', 'Services')], limit=1)
                if parent_menu:
                    keeper_vals['parent_id'] = parent_menu.id
                elif main_menu:
                    keeper_vals['parent_id'] = main_menu.id
            elif main_menu:
                keeper_vals['parent_id'] = main_menu.id

            keeper.write(keeper_vals)

            # Unlink ALL other matching duplicates
            duplicates = all_matches.filtered(lambda m: m.id != keeper.id)
            if duplicates:
                _logger.info(
                    "Purging %d duplicate menus for '%s' (Keeper ID: %s, Duplicates IDs: %s)",
                    len(duplicates), spec['name'], keeper.id, duplicates.ids
                )
                for dup in duplicates:
                    try:
                        dup.unlink()
                    except Exception as e:
                        _logger.warning("Could not unlink duplicate menu %s: %s", dup.id, e)

        # 5. Pre-fill Homepage SEO in website.page
        home_pages = self.env['website.page'].sudo().search([
            ('url', 'in', ['/', '/home']),
        ])
        seo_title = "ERP Odoo 18 Laos | SME ERP, POS, Website & TaxRIS Integration | Nahan"
        seo_desc = (
            "Nahan.app provides Odoo 18 ERP implementation, POS, CRM, Accounting, "
            "Inventory Management, Website Development, eCommerce, and TaxRIS API Integration "
            "for SMEs and Startups in Laos."
        )
        for page in home_pages:
            page.write({
                'website_meta_title': seo_title,
                'website_meta_description': seo_desc,
            })

        return True

    @api.model
    def setup_website_navigation_and_seo(self):
        """Backward-compatible alias for cleanup_duplicate_menus."""
        return self.cleanup_duplicate_menus()
