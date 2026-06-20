(function () {
  'use strict';

  // ── Utility ──────────────────────────────────────────────────────────────

  function $(selector, context) {
    return (context || document).querySelector(selector);
  }

  function $$(selector, context) {
    return Array.from((context || document).querySelectorAll(selector));
  }

  function on(el, event, handler, options) {
    if (el) el.addEventListener(event, handler, options || false);
  }

  // ── Toast ─────────────────────────────────────────────────────────────────

  function showToast(message, duration) {
    var existing = $('#mtl-toast');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.id = 'mtl-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.textContent = message;

    Object.assign(toast.style, {
      position: 'fixed',
      bottom: '1.5rem',
      left: '50%',
      transform: 'translateX(-50%) translateY(1rem)',
      background: '#1e293b',
      color: '#f8fafc',
      padding: '0.6rem 1.2rem',
      borderRadius: '0.5rem',
      fontSize: '0.875rem',
      zIndex: '9999',
      opacity: '0',
      transition: 'opacity 0.25s ease, transform 0.25s ease',
      pointerEvents: 'none',
      whiteSpace: 'nowrap'
    });

    document.body.appendChild(toast);

    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(-50%) translateY(0)';
      });
    });

    setTimeout(function () {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(1rem)';
      setTimeout(function () { toast.remove(); }, 300);
    }, duration || 2000);
  }

  // ── Copy ──────────────────────────────────────────────────────────────────

  function copyText(text, button) {
    if (!text) return;

    function onSuccess() {
      showToast('Copied!');
      if (button) {
        var original = button.textContent;
        button.textContent = 'Copied!';
        button.disabled = true;
        setTimeout(function () {
          button.textContent = original;
          button.disabled = false;
        }, 1500);
      }
    }

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(onSuccess).catch(function () {
        fallbackCopy(text, onSuccess);
      });
    } else {
      fallbackCopy(text, onSuccess);
    }
  }

  function fallbackCopy(text, callback) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      document.execCommand('copy');
      if (callback) callback();
    } catch (e) {
      showToast('Copy failed');
    }
    document.body.removeChild(ta);
  }

  function initCopyButtons() {
    $$('[data-copy]').forEach(function (btn) {
      on(btn, 'click', function () {
        var target = btn.dataset.copy;
        var source = target ? $(target) : null;
        var text = source
          ? (source.value !== undefined ? source.value : source.textContent)
          : btn.dataset.copyText || '';
        copyText(text, btn);
      });
    });
  }

  // ── Clear ─────────────────────────────────────────────────────────────────

  function clearField(el) {
    if (!el) return;
    if (el.value !== undefined) {
      el.value = '';
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
      el.textContent = '';
    }
    el.focus();
  }

  function initClearButtons() {
    $$('[data-clear]').forEach(function (btn) {
      on(btn, 'click', function () {
        var targets = btn.dataset.clear
          ? btn.dataset.clear.split(',').map(function (s) { return s.trim(); })
          : [];
        if (targets.length) {
          targets.forEach(function (sel) { clearField($(sel)); });
        }
      });
    });
  }

  // ── FAQ Accordion ─────────────────────────────────────────────────────────

  function initAccordion() {
    $$('.faq-item, [data-accordion-item]').forEach(function (item) {
      var trigger = $('[data-accordion-trigger], .faq-question', item) || item.firstElementChild;
      var panel   = $('[data-accordion-panel], .faq-answer', item);

      if (!trigger || !panel) return;

      if (!trigger.id) trigger.id = 'mtl-trigger-' + Math.random().toString(36).slice(2);
      if (!panel.id)   panel.id   = 'mtl-panel-'   + Math.random().toString(36).slice(2);

      trigger.setAttribute('aria-controls', panel.id);
      trigger.setAttribute('aria-expanded', 'false');
      trigger.setAttribute('role', 'button');
      if (!trigger.hasAttribute('tabindex')) trigger.setAttribute('tabindex', '0');

      panel.setAttribute('role', 'region');
      panel.setAttribute('aria-labelledby', trigger.id);
      panel.hidden = true;

      function toggle() {
        var open = trigger.getAttribute('aria-expanded') === 'true';
        trigger.setAttribute('aria-expanded', String(!open));
        panel.hidden = open;
        item.classList.toggle('is-open', !open);
      }

      on(trigger, 'click', toggle);
      on(trigger, 'keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggle();
        }
      });
    });
  }

  // ── Animated Counter ──────────────────────────────────────────────────────

  function animateCount(el, end, duration) {
    var start = 0;
    var startTime = null;
    var numEnd = parseFloat(end);
    var isFloat = String(end).includes('.');
    var decimals = isFloat ? (String(end).split('.')[1] || '').length : 0;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / (duration || 800), 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = start + (numEnd - start) * eased;
      el.textContent = isFloat ? current.toFixed(decimals) : Math.floor(current).toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = isFloat ? numEnd.toFixed(decimals) : numEnd.toLocaleString();
    }

    requestAnimationFrame(step);
  }

  function initStatCounters() {
    var counters = $$('[data-count]');
    if (!counters.length) return;

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var el = entry.target;
            animateCount(el, el.dataset.count, parseInt(el.dataset.countDuration, 10) || 800);
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.3 });

      counters.forEach(function (el) { observer.observe(el); });
    } else {
      counters.forEach(function (el) {
        animateCount(el, el.dataset.count, 800);
      });
    }
  }

  // ── Character / Word Counter ──────────────────────────────────────────────

  function initInputCounters() {
    $$('[data-char-count], [data-word-count]').forEach(function (input) {
      var charTarget = input.dataset.charCount ? $(input.dataset.charCount) : null;
      var wordTarget = input.dataset.wordCount ? $(input.dataset.wordCount) : null;

      function update() {
        var val = input.value;
        if (charTarget) charTarget.textContent = val.length;
        if (wordTarget) {
          var words = val.trim() ? val.trim().split(/\s+/).length : 0;
          wordTarget.textContent = words;
        }
      }

      on(input, 'input', update);
      update();
    });
  }

  // ── File Drop Zone ────────────────────────────────────────────────────────

  function initDropZones() {
    $$('[data-dropzone]').forEach(function (zone) {
      var inputSel = zone.dataset.dropzone;
      var fileInput = inputSel ? $(inputSel) : $('input[type="file"]', zone);

      function highlight() { zone.classList.add('drag-over'); }
      function unhighlight() { zone.classList.remove('drag-over'); }

      on(zone, 'dragenter', function (e) { e.preventDefault(); highlight(); });
      on(zone, 'dragover',  function (e) { e.preventDefault(); highlight(); });
      on(zone, 'dragleave', unhighlight);
      on(zone, 'drop', function (e) {
        e.preventDefault();
        unhighlight();
        if (fileInput && e.dataTransfer.files.length) {
          fileInput.files = e.dataTransfer.files;
          fileInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        zone.dispatchEvent(new CustomEvent('mtl:drop', { detail: { files: e.dataTransfer.files }, bubbles: true }));
      });

      on(zone, 'click', function () { if (fileInput) fileInput.click(); });
      on(zone, 'keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (fileInput) fileInput.click(); }
      });

      if (!zone.hasAttribute('tabindex')) zone.setAttribute('tabindex', '0');
      zone.setAttribute('role', 'button');
    });
  }

  // ── Tab Panels ────────────────────────────────────────────────────────────

  function initTabs() {
    $$('[role="tablist"]').forEach(function (tablist) {
      var tabs   = $$('[role="tab"]', tablist);
      var panels = tabs.map(function (t) { return $(t.getAttribute('aria-controls')); });

      function activate(tab) {
        tabs.forEach(function (t, i) {
          var active = t === tab;
          t.setAttribute('aria-selected', String(active));
          t.setAttribute('tabindex', active ? '0' : '-1');
          if (panels[i]) panels[i].hidden = !active;
        });
        tab.focus();
      }

      tabs.forEach(function (tab) {
        on(tab, 'click', function () { activate(tab); });
        on(tab, 'keydown', function (e) {
          var idx = tabs.indexOf(tab);
          if (e.key === 'ArrowRight') { e.preventDefault(); activate(tabs[(idx + 1) % tabs.length]); }
          if (e.key === 'ArrowLeft')  { e.preventDefault(); activate(tabs[(idx - 1 + tabs.length) % tabs.length]); }
          if (e.key === 'Home')       { e.preventDefault(); activate(tabs[0]); }
          if (e.key === 'End')        { e.preventDefault(); activate(tabs[tabs.length - 1]); }
        });
      });
    });
  }

  // ── Mobile Nav Toggle ─────────────────────────────────────────────────────

  function initNavToggle() {
    var toggle = $('#nav-toggle, [data-nav-toggle]');
    var nav    = $('#nav-menu, [data-nav-menu]');
    if (!toggle || !nav) return;

    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', nav.id || 'nav-menu');

    on(toggle, 'click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });

    on(document, 'keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  // ── Init ──────────────────────────────────────────────────────────────────

  function init() {
    initCopyButtons();
    initClearButtons();
    initAccordion();
    initStatCounters();
    initInputCounters();
    initDropZones();
    initTabs();
    initNavToggle();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.MTL = {
    showToast: showToast,
    copyText: copyText,
    clearField: clearField,
    animateCount: animateCount
  };
}());