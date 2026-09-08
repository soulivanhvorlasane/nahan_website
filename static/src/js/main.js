/** @odoo-module **/

// Part of Nahan.app. See LICENSE file for full copyright and licensing details.

/**
 * Nahan.app Corporate Website Public Interaction Script
 * Compatible with Odoo 18 frontend architecture.
 */

document.addEventListener('DOMContentLoaded', () => {
    initDynamicCounters();
    initConsultationForm();
    initSmoothScroll();
    initActiveNav();
    initServicesDropdownHover();
    initBrandLogoNav();
    initSearchModal();
});

/**
 * 1. Animated Dynamic Counters
 * Increases numerical values when the stats bar enters the viewport.
 */
function initDynamicCounters() {
    const statCounters = document.querySelectorAll('.stat-number[data-target]');
    if (!statCounters.length) return;

    let hasAnimated = false;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                statCounters.forEach((counter) => {
                    const target = parseInt(counter.getAttribute('data-target'), 10);
                    if (isNaN(target)) return;

                    const raw = counter.getAttribute('data-raw') || '';
                    const suffix = raw.replace(/\d+/g, '').trim() || '+';
                    const valEl = counter.querySelector('.stat-val') || counter;

                    const duration = 1600; // ms
                    const stepTime = 25;
                    const steps = duration / stepTime;
                    const increment = target / steps;
                    let current = 0;

                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            valEl.textContent = raw || (target + suffix);
                            clearInterval(timer);
                        } else {
                            valEl.textContent = Math.floor(current) + suffix;
                        }
                    }, stepTime);
                });
            }
        });
    }, { threshold: 0.2 });

    const statsBar = document.querySelector('.nahan-stats-bar');
    if (statsBar) {
        observer.observe(statsBar);
    }
}

/**
 * 2. Interactive AJAX Consultation Form Handler
 * Validates form and submits data to Odoo backend CRM lead endpoint without page refresh.
 */
function initConsultationForm() {
    const form = document.getElementById('nahanConsultationForm');
    if (!form) return;

    const submitBtn = form.querySelector('.btn-consultation-submit');
    const responseBox = document.getElementById('nahanFormResponse');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Collect inputs
        const companyName = (form.querySelector('[name="company_name"]')?.value || '').trim();
        const contactName = (form.querySelector('[name="contact_name"]')?.value || '').trim();
        const phone = (form.querySelector('[name="phone"]')?.value || '').trim();
        const email = (form.querySelector('[name="email"]')?.value || '').trim();
        const businessType = form.querySelector('[name="business_type"]')?.value || '';
        const employeeCount = form.querySelector('[name="employee_count"]')?.value || '';
        const message = (form.querySelector('[name="message"]')?.value || '').trim();

        // Collect multi-select service checkboxes
        const selectedServices = [];
        form.querySelectorAll('input[name="services"]:checked').forEach((cb) => {
            selectedServices.push(cb.value);
        });

        // Basic client-side validation
        if (!contactName && !companyName) {
            showAlert(responseBox, 'danger', 'Please enter your Contact Name or Company Name.');
            return;
        }

        if (!phone && !email) {
            showAlert(responseBox, 'danger', 'Please provide a Phone Number or Email address so we can reach you.');
            return;
        }

        // Set loading state
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span> Submitting...';
        clearAlert(responseBox);

        const payload = {
            company_name: companyName,
            contact_name: contactName,
            phone: phone,
            email: email,
            business_type: businessType,
            employee_count: employeeCount,
            interested_services: selectedServices,
            message: message,
        };

        try {
            const response = await fetch('/api/consultation/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ params: payload }),
            });

            const result = await response.json();
            const resData = result.result || result;

            if (resData && resData.success) {
                // Success state: hide form and show celebratory card
                form.style.display = 'none';
                const successMsg = resData.message || 'Thank you! We will get back to you shortly.';
                showAlert(
                    responseBox,
                    'success',
                    `<div class="text-center py-4">
                        <div class="mb-3" style="font-size: 3rem;">🎉</div>
                        <h4 class="fw-bold text-success mb-2">Request Received!</h4>
                        <p class="text-muted mb-4">${successMsg}</p>
                        <button type="button" class="btn btn-outline-secondary btn-sm" onclick="location.reload()">
                            Submit Another Request
                        </button>
                    </div>`
                );
            } else {
                const errorMsg = resData?.message || resData?.error || 'Failed to submit request. Please contact us via phone or WhatsApp.';
                showAlert(responseBox, 'danger', errorMsg);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
            }
        } catch (err) {
            console.error('Nahan Form submission error:', err);
            showAlert(responseBox, 'danger', 'A network error occurred. Please call or WhatsApp us at +856 20 5274 6767.');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
}

function showAlert(container, type, message) {
    if (!container) return;
    container.innerHTML = `
        <div class="alert alert-${type} shadow-sm border-0 fade show" role="alert">
            ${message}
        </div>
    `;
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function clearAlert(container) {
    if (container) {
        container.innerHTML = '';
    }
}

/**
 * 3. Smooth anchor scrolling for CTA links (#consultation)
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start',
                });
            }
        });
    });
}

/**
 * 4. Dynamic Active Navigation Manager & ScrollSpy
 * Ensures active menu highlighting accurately reflects current page, anchor, and scroll position.
 * Eliminates active background being stuck on "Services" when clicking other section anchors or pages.
 */
function initActiveNav() {
    const allNavItems = document.querySelectorAll(
        '.nahan-nav-links .nav-link, .nahan-nav-links .dropdown-item, .nahan-mobile-nav-list .nav-link'
    );
    if (!allNavItems.length) return;

    function getNormalizedPath() {
        let p = window.location.pathname.toLowerCase();
        // Strip language prefixes like /lo, /en, /lo_la, /en_us
        p = p.replace(/^\/(lo|en|lo_la|en_us)(?=\/|$)/, '') || '/';
        return p;
    }

    function setActiveLink(targetKey) {
        allNavItems.forEach((link) => {
            const key = link.getAttribute('data-nav-key');
            let shouldBeActive = false;

            if (key === targetKey) {
                shouldBeActive = true;
            }

            // When viewing any services item (erp, api, services-overview, services),
            // the parent Services dropdown toggle must always remain active!
            if (['erp', 'api', 'services-overview', 'services'].includes(targetKey)) {
                if (key === 'services') {
                    shouldBeActive = true;
                }
                if (targetKey === 'services' && key === 'services-overview') {
                    shouldBeActive = true;
                }
            }

            if (shouldBeActive) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    function updateActiveByLocation() {
        const path = getNormalizedPath();
        const hash = (window.location.hash || '').toLowerCase();

        if (path === '/' || path === '') {
            setActiveLink('home');
        } else if (path.startsWith('/services')) {
            if (hash === '#erp') {
                setActiveLink('erp');
            } else if (hash === '#api' || hash === '#taxris') {
                setActiveLink('api');
            } else {
                setActiveLink('services');
            }
        } else if (path.includes('/blog')) {
            setActiveLink('blog');
        } else if (path.includes('/about')) {
            setActiveLink('about');
        } else if (path.includes('/contact')) {
            setActiveLink('contact');
        }
    }

    // Handle clicks directly on navigation items
    allNavItems.forEach((link) => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href') || '';
            const key = this.getAttribute('data-nav-key');
            const currentPath = getNormalizedPath();

            // If on /services and clicking an anchor or sub-item
            if (currentPath.startsWith('/services')) {
                if (href.includes('#erp') || key === 'erp') {
                    e.preventDefault();
                    setActiveLink('erp');
                    const target = document.getElementById('erp');
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                    if (window.history && window.history.pushState) {
                        window.history.pushState(null, '', '#erp');
                    }
                    return;
                } else if (href.includes('#api') || href.includes('#taxris') || key === 'api') {
                    e.preventDefault();
                    setActiveLink('api');
                    const target = document.getElementById('api') || document.getElementById('taxris');
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                    if (window.history && window.history.pushState) {
                        window.history.pushState(null, '', '#api');
                    }
                    return;
                } else if (key === 'services-overview' || href === '/services' || href.endsWith('/services')) {
                    if (link.classList.contains('dropdown-toggle')) {
                        // Let dropdown toggle open on mobile/click
                        return;
                    }
                    e.preventDefault();
                    setActiveLink('services');
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    if (window.history && window.history.pushState) {
                        window.history.pushState(null, '', window.location.pathname);
                    }
                    return;
                }
            }

            // Normal click on any other link
            if (key) {
                setActiveLink(key);
            }
        });
    });

    // ScrollSpy for /services page: dynamically updates active menu as user scrolls
    if (getNormalizedPath().startsWith('/services')) {
        let scrollTimeout = null;

        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                const scrollPos = window.scrollY + 200;
                const erpEl = document.getElementById('erp');
                const apiEl = document.getElementById('api') || document.getElementById('taxris');

                const sections = [
                    { key: 'services', top: 0 },
                ];
                if (erpEl) sections.push({ key: 'erp', top: erpEl.offsetTop });
                if (apiEl) sections.push({ key: 'api', top: apiEl.offsetTop });

                sections.sort((a, b) => b.top - a.top); // Highest top first
                for (const sec of sections) {
                    if (scrollPos >= sec.top) {
                        setActiveLink(sec.key);
                        break;
                    }
                }
            }, 50);
        }, { passive: true });
    }

    // Initial check on page load & hash changes
    updateActiveByLocation();
    window.addEventListener('hashchange', updateActiveByLocation);
    window.addEventListener('popstate', updateActiveByLocation);
}

/**
 * 5. Smooth Services Dropdown Hover with Grace Delay
 * Solves the issue where moving cursor diagonally or across gaps causes dropdown to disappear.
 * Provides a 220ms grace window on mouseleave before closing.
 */
function initServicesDropdownHover() {
    const dropdown = document.querySelector('.nahan-services-dropdown');
    if (!dropdown) return;

    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
    if (!toggle || !menu) return;

    let closeTimer = null;

    function openMenu() {
        if (window.innerWidth < 992) return;
        if (closeTimer) {
            clearTimeout(closeTimer);
            closeTimer = null;
        }
        dropdown.classList.add('is-hovered');
        menu.classList.add('show');
        toggle.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
        if (window.innerWidth < 992) return;
        if (closeTimer) {
            clearTimeout(closeTimer);
        }
        closeTimer = setTimeout(() => {
            dropdown.classList.remove('is-hovered');
            menu.classList.remove('show');
            toggle.setAttribute('aria-expanded', 'false');
        }, 220); // 220ms grace window ensures smooth diagonal cursor movement
    }

    // Bind listeners to parent container, toggle, and dropdown menu
    dropdown.addEventListener('mouseenter', openMenu);
    dropdown.addEventListener('mouseleave', closeMenu);
    menu.addEventListener('mouseenter', openMenu);
    menu.addEventListener('mouseleave', closeMenu);

    // Auto-close menu when a dropdown item is clicked
    menu.querySelectorAll('.dropdown-item').forEach((item) => {
        item.addEventListener('click', () => {
            if (closeTimer) clearTimeout(closeTimer);
            dropdown.classList.remove('is-hovered');
            menu.classList.remove('show');
            toggle.setAttribute('aria-expanded', 'false');
        });
    });
}

/**
 * 6. Brand Logo Navigation Handler
 * Ensures clicking brand logo or header icons always navigates reliably to the active language home (/lo in Lao, / in English),
 * resolving any default-prevention issues or event bubbling blocks.
 */
function initBrandLogoNav() {
    const brandElements = document.querySelectorAll('.navbar-brand, .nahan-mobile-drawer .offcanvas-header a');
    brandElements.forEach((brand) => {
        brand.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href && href !== '#' && href !== '') {
                setTimeout(() => {
                    if (e.defaultPrevented) {
                        window.location.href = href;
                    }
                }, 50);
            }
        });
    });
}

/**
 * 7. Search Modal Auto-focus Handler
 * Ensures search input is immediately focused when modal is opened for seamless UX.
 */
function initSearchModal() {
    const searchModal = document.getElementById('o_search_modal');
    if (!searchModal) return;

    searchModal.addEventListener('shown.bs.modal', () => {
        const searchInput = searchModal.querySelector('input[name="search"], input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    });
}


