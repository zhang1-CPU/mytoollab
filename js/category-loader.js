/**
 * Category Loader - dynamically renders tool cards on category pages
 * Reads /tools-index.json, filters by category, renders grid
 */
(function() {
  // Determine category from URL: /categories/seo.html -> "seo"
  function getCategoryFromURL() {
    var path = window.location.pathname;
    var match = path.match(/\/categories\/([^\/]+)\.html?$/i);
    if (match) return match[1].toLowerCase();
    return null;
  }

  // Capitalize first letter to match category names in JSON
  function capitalize(s) {
    if (!s) return s;
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  // Special-case category slugs to JSON category names
  // Tools-index.json stores category names with this exact capitalization
  function getCategoryName(slug) {
    var map = {
      'pdf': 'PDF',
      'seo': 'SEO',
      'dev': 'Developer',
      'developer': 'Developer'
    };
    if (map[slug]) return map[slug];
    return capitalize(slug);
  }

  // Render tool card HTML — matches existing category page styles
  function renderCard(tool) {
    var icon = tool.icon || '🔧';
    var name = tool.name || 'Untitled';
    var desc = tool.description || '';
    var url = tool.url || '#';
    // PDF page uses BEM-style classes (tool-card__icon, tool-card__title, etc.)
    if (document.body.classList.contains('pdf-page') || document.querySelector('.tool-card__icon')) {
      return '<a class="tool-card" href="' + escapeHTML(url) + '">' +
        '<div class="tool-card__icon">' + escapeHTML(icon) + '</div>' +
        '<div class="tool-card__title">' + escapeHTML(name) + '</div>' +
        '<div class="tool-card__desc">' + escapeHTML(desc) + '</div>' +
        '<div class="tool-card__cta">Open tool &rarr;</div>' +
        '</a>';
    }
    // Default: article card matching text/image/generator/calculator style
    // Use h3 to match existing category page CSS (.tool-card h3 {...})
    return '<article class="tool-card">' +
      '<div class="tool-icon" aria-hidden="true">' + escapeHTML(icon) + '</div>' +
      '<h3>' + escapeHTML(name) + '</h3>' +
      '<p>' + escapeHTML(desc) + '</p>' +
      '<a href="' + escapeHTML(url) + '" class="tool-link">Open tool</a>' +
      '</article>';
  }

  function escapeHTML(s) {
    return String(s).replace(/[&<>"']/g, function(c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // Find the existing tools-grid container; create one if missing
  function getOrCreateGrid() {
    var existing = document.querySelector('.tools-grid');
    if (existing) return existing;
    // Find an h1 and insert grid after the hero section
    var h1 = document.querySelector('h1');
    if (!h1) return null;
    var grid = document.createElement('div');
    grid.className = 'tools-grid';
    var section = h1.closest('.hero, .container-md, section, main, .section');
    if (section && section.parentElement) {
      section.parentElement.insertBefore(grid, section.nextSibling);
    } else {
      h1.parentElement.appendChild(grid);
    }
    return grid;
  }

  function renderCategory() {
    var categorySlug = getCategoryFromURL();
    if (!categorySlug) return;
    var categoryName = getCategoryName(categorySlug);
    var grid = getOrCreateGrid();
    if (!grid) return;

    grid.innerHTML = '<div class="loading-msg" style="padding:24px;text-align:center;color:var(--text-muted,#64748b);">Loading tools…</div>';

    // Fetch with timeout fallback to embedded backup
    var timeout = setTimeout(function() {
      if (grid.querySelector('.loading-msg')) {
        grid.innerHTML = window.__categoryBackup || '<div class="loading-msg" style="padding:24px;text-align:center;color:var(--text-muted,#64748b);">Loading tools…</div>';
      }
    }, 5000);

    fetch('/tools-index.json', { cache: 'no-cache' })
      .then(function(r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function(data) {
        clearTimeout(timeout);
        var filtered = (data || []).filter(function(t) {
          return (t.category || '') === categoryName;
        });
        if (filtered.length === 0) {
          grid.innerHTML = '<div class="loading-msg" style="padding:24px;text-align:center;color:var(--text-muted,#64748b);">No tools in this category yet.</div>';
          return;
        }
        filtered.sort(function(a, b) { return (a.name || '').localeCompare(b.name || ''); });
        grid.innerHTML = filtered.map(renderCard).join('');
        if (!document.getElementById('category-loader-styles')) {
          var s = document.createElement('style');
          s.id = 'category-loader-styles';
          s.textContent = '.tools-grid .tool-card{display:block;color:inherit;text-decoration:none;}' +
            '.tools-grid .tool-card a.tool-link{display:inline-block;margin-top:8px;color:var(--primary,#2563eb);text-decoration:none;font-size:.85rem;font-weight:500;}' +
            '.tools-grid .tool-card a.tool-link:hover{text-decoration:underline;}' +
            '[data-theme="dark"] .tools-grid .tool-card{background:var(--card,#1e293b)!important;border-color:var(--border,#334155)!important;}';
          document.head.appendChild(s);
        }
      })
      .catch(function(err) {
        clearTimeout(timeout);
        console.warn('Category loader failed:', err);
        // Fallback to embedded backup if available
        if (window.__categoryBackup) {
          grid.innerHTML = window.__categoryBackup;
        } else {
          grid.innerHTML = '<div class="loading-msg" style="padding:24px;text-align:center;color:var(--text-muted,#64748b);">Unable to load tools. <a href="/">Return to home</a></div>';
        }
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderCategory);
  } else {
    renderCategory();
  }
})();
