/* Progressive gallery: the server-rendered scroll-snap strip works without JavaScript. */
window.novaGallery = function () {
  return {
    current: 0, count: 0,
    init() { this.count = this.$refs.track.children.length; },
    go(index) {
      this.current = (index + this.count) % this.count;
      const track = this.$refs.track;
      track.scrollTo({left: this.current * track.clientWidth,
        behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
      window.novaTrack?.('activity_gallery_interaction', {image_index: this.current + 1});
    },
    sync() { this.current = Math.round(this.$refs.track.scrollLeft / this.$refs.track.clientWidth); }
  };
};

document.addEventListener('DOMContentLoaded', () => {
  const config = document.getElementById('nova-analytics-config');
  const identifier = config?.dataset.measurementId || '';
  let active = false;
  const panel = document.getElementById('nova-consent');
  let preference = null;
  try { preference = localStorage.getItem('nova_analytics'); } catch (_) {}
  const properties = () => {
    const page = document.querySelector('[data-activity-slug]');
    const data = {
      activity_slug: page?.dataset.activitySlug || '',
      tour_type: page?.dataset.tourType || '',
      source_surface: config?.dataset.sourceSurface || '',
      utm_campaign: config?.dataset.utmCampaign || '',
      utm_content: config?.dataset.utmContent || '',
    };
    if (page?.dataset.durationMinutes) data.duration_minutes = Number(page.dataset.durationMinutes);
    if (page?.dataset.priceCurrency) data.price_currency = page.dataset.priceCurrency;
    if (page?.dataset.pricingModel) data.pricing_model = page.dataset.pricingModel;
    const price = Number(page?.dataset.priceValue);
    if (page?.dataset.priceValue && Number.isFinite(price)) data.price_value = price;
    return data;
  };
  window.novaTrack = (name, details = {}) => {
    if (!active || !window.gtag) return;
    // Only code-defined non-personal fields enter analytics. Never copy hrefs, form values or WhatsApp messages.
    const allowed = [
      'activity_slug', 'related_activity_slug', 'service_slug', 'cta_location',
      'image_index', 'tour_type', 'duration_minutes', 'price_currency',
      'price_value', 'pricing_model', 'source_surface', 'utm_campaign', 'utm_content',
    ];
    const safe = Object.fromEntries(Object.entries(details).filter(([key]) => allowed.includes(key)));
    window.gtag('event', name, {...properties(), ...safe});
  };
  function enable() {
    if (!/^G-[A-Z0-9]+$/.test(identifier) || active) return;
    active = true;
    window['ga-disable-' + identifier] = false;
    if (!window.gtag) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      const script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + identifier;
      document.head.appendChild(script);
      window.gtag('js', new Date());
      let referrer = '';
      try { const url = new URL(document.referrer); referrer = url.origin + url.pathname; } catch (_) {}
      const page = {page_location: location.origin + location.pathname, page_referrer: referrer};
      window.gtag('config', identifier, {...page, send_page_view: false, allow_google_signals: false});
      window.gtag('event', 'page_view', page);
    }
    if (document.querySelector('.activity-page')) window.novaTrack('activity_view');
    if (document.querySelector('.activity-service-card')) window.novaTrack('service_view');
  }
  function choose(value) {
    try { localStorage.setItem('nova_analytics', value); } catch (_) {}
    if (panel) panel.hidden = true;
    if (value === 'yes') enable();
    else { active = false; window['ga-disable-' + identifier] = true; }
  }
  if (/^G-[A-Z0-9]+$/.test(identifier)) {
    if (preference === 'yes') enable();
    else if (preference !== 'no' && panel) panel.hidden = false;
  }
  document.querySelectorAll('[data-analytics-choice]').forEach(button => button.addEventListener('click', () => choose(button.dataset.analyticsChoice)));
  document.querySelector('[data-analytics-settings]')?.addEventListener('click', () => { if (panel) panel.hidden = false; });
  document.addEventListener('click', event => {
    const link = event.target.closest('[data-nova-event]');
    if (link) window.novaTrack(link.dataset.novaEvent, {
      activity_slug: link.dataset.activitySlug || properties().activity_slug,
      related_activity_slug: link.dataset.relatedActivitySlug || '',
      service_slug: link.dataset.serviceSlug || '', cta_location: link.dataset.ctaLocation || 'content'});
  });
  document.addEventListener('change', event => {
    const form = event.target.closest('form[data-nova-event="hotel_access_check"]');
    if (form) window.novaTrack('hotel_access_check', {cta_location: 'hotel_checker'});
  });
  document.body.addEventListener('booking_enquiry_submit', event => {
    window.novaTrack('booking_enquiry_submit', {activity_slug: event.detail?.activity_slug || ''});
  });
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { window.novaTrack(entry.target.dataset.novaObserve); observer.unobserve(entry.target); }
  }), {threshold: 0.35});
  document.querySelectorAll('[data-nova-observe]').forEach(element => observer.observe(element));
  const success = document.querySelector('[data-enquiry-submitted=true]');
  if (success) window.novaTrack('booking_enquiry_submit', {activity_slug: success.dataset.activitySlug || ''});
});
