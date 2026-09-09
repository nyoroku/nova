/**
 * Rafiki Boat Rides - Main JavaScript File
 * Handles UI interactions, HTMX enhancements, and other client-side functionality.
 */

(function () {
    'use strict';

    // Wait for the DOM to be fully loaded before running scripts
    document.addEventListener('DOMContentLoaded', function () {

        // --- 1. Mobile Navbar Toggle ---
        function initNavbar() {
            // Get all "navbar-burger" elements
            const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

            // Check if there are any navbar burgers
            if ($navbarBurgers.length > 0) {
                // Add a click event on each of them
                $navbarBurgers.forEach(el => {
                    el.addEventListener('click', () => {
                        // Get the target from the "data-target" attribute
                        const target = el.dataset.target;
                        const $target = document.getElementById(target);

                        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                        el.classList.toggle('is-active');
                        $target.classList.toggle('is-active');
                    });
                });
            }
        }

        // --- 2. Notification (Message) Dismissal ---
        function initNotifications() {
            // Get all "delete" buttons within notifications
            const $notifications = Array.prototype.slice.call(document.querySelectorAll('.notification .delete'), 0);

            if ($notifications.length > 0) {
                $notifications.forEach(el => {
                    el.addEventListener('click', () => {
                        // Find the parent notification element and remove it
                        const notification = el.parentElement;
                        notification.remove();
                    });
                });
            }
        }

        // --- 3. HTMX Enhancements ---
        function initHtmxEnhancements() {
            // Add a loading indicator to any element with 'htmx-indicator' class
            htmx.on('htmx:beforeRequest', function (evt) {
                const indicator = document.querySelector(evt.target.getAttribute('hx-indicator'));
                if (indicator) {
                    indicator.classList.add('htmx-request');
                }
            });

            htmx.on('htmx:afterRequest', function (evt) {
                const indicator = document.querySelector(evt.target.getAttribute('hx-indicator'));
                if (indicator) {
                    indicator.classList.remove('htmx-request');
                }
            });

            // Add a subtle fade-in effect to content swapped by HTMX
            htmx.on('htmx:afterSwap', function (evt) {
                const swappedContent = evt.detail.target;
                swappedContent.style.opacity = '0';
                swappedContent.style.transition = 'opacity 0.4s ease-in-out';

                // Use a timeout to ensure the transition applies
                setTimeout(() => {
                    swappedContent.style.opacity = '1';
                }, 10);

                // Re-initialize notifications for new content that might contain them
                initNotifications();
            });
        }

        // --- 4. Form Focus Enhancement ---
        function initFormFocus() {
            const inputs = document.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('focus', () => {
                    input.parentElement.classList.add('is-focused');
                });
                input.addEventListener('blur', () => {
                    if (input.value === '') {
                        input.parentElement.classList.remove('is-focused');
                    }
                });
            });
        }

        // --- Initialize all functions ---
        initNavbar();
        initNotifications();
        initHtmxEnhancements();
        initFormFocus();

    });

})();
// ========================================
// QUICK IMAGE OPTIMIZATION - 15 MINUTE FIX
// Add this to your main.js
// ========================================

document.addEventListener('DOMContentLoaded', function () {

    // ========================================
    // 1. IMAGE SAFETY (Force Opacity)
    // ========================================
    document.querySelectorAll('img').forEach(img => {
        img.style.opacity = '1';
        img.classList.add('loaded');
    });

    // ========================================
    // 2. ADD LOADING PLACEHOLDERS
    // ========================================
    function addImagePlaceholders() {
        document.querySelectorAll('img:not(.has-placeholder)').forEach(img => {
            if (!img.complete) {
                // Add loading class
                img.classList.add('image-loading');
                img.classList.add('has-placeholder');

                // Remove when loaded
                img.addEventListener('load', function () {
                    this.classList.remove('image-loading');
                });
            }
        });
    }

    addImagePlaceholders();

    // ========================================
    // 3. OPTIMIZE IMAGES ON THE FLY
    // ========================================
    function optimizeImages() {
        const images = document.querySelectorAll('img:not([width]):not([height])');

        images.forEach(img => {
            // Add loading attribute if missing
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }

            // Add decode async for better performance
            if (!img.hasAttribute('decoding')) {
                img.setAttribute('decoding', 'async');
            }

            // If image is loaded, get its dimensions
            if (img.complete && img.naturalWidth > 0) {
                if (!img.hasAttribute('width')) {
                    img.setAttribute('width', img.naturalWidth);
                }
                if (!img.hasAttribute('height')) {
                    img.setAttribute('height', img.naturalHeight);
                }
            }
        });
    }

    optimizeImages();

    // ========================================
    // 4. PRELOAD CRITICAL IMAGES
    // ========================================
    function preloadCriticalImages() {
        // Preload hero image
        const heroImage = document.querySelector('.hero img, .hero [style*="background-image"]');
        if (heroImage) {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';

            if (heroImage.tagName === 'IMG') {
                link.href = heroImage.src;
            } else {
                const bgImage = heroImage.style.backgroundImage;
                const urlMatch = bgImage.match(/url\(['"]?([^'"]+)['"]?\)/);
                if (urlMatch) {
                    link.href = urlMatch[1];
                }
            }

            if (link.href) {
                document.head.appendChild(link);
            }
        }
    }

    preloadCriticalImages();

    // ========================================
    // 5. IMAGE ERROR HANDLING
    // ========================================
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function () {
            // Prevent infinite error loop
            if (!this.dataset.errorHandled) {
                this.dataset.errorHandled = 'true';

                // Try to load a placeholder
                this.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"%3E%3Crect fill="%23f0f0f0" width="400" height="300"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" fill="%23999" font-family="Arial" font-size="18"%3EImage not available%3C/text%3E%3C/svg%3E';

                console.warn('Image failed to load:', this.dataset.src || this.src);
            }
        });
    });

    // ========================================
    // 6. MONITOR IMAGE LOADING PERFORMANCE
    // ========================================
    if (window.PerformanceObserver) {
        const imageObserver = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.initiatorType === 'img') {
                    const loadTime = entry.responseEnd - entry.startTime;

                    if (loadTime > 2000) {
                        console.warn(`Slow image detected (${Math.round(loadTime)}ms):`, entry.name);
                    }
                }
            }
        });

        imageObserver.observe({ entryTypes: ['resource'] });
    }

    // ========================================
    // 7. RESPONSIVE IMAGE LOADING
    // ========================================
    function loadResponsiveImages() {
        document.querySelectorAll('[data-src-mobile][data-src-desktop]').forEach(img => {
            const isMobile = window.innerWidth < 768;
            const src = isMobile ? img.dataset.srcMobile : img.dataset.srcDesktop;

            if (src && img.src !== src) {
                img.src = src;
            }
        });
    }

    loadResponsiveImages();

    // Reload on resize (debounced)
    let resizeTimeout;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(loadResponsiveImages, 300);
    });
});

