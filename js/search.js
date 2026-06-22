/**
 * Site Search Component
 * - Loads tools-index.json
 * - Real-time search with debounce
 * - Keyboard navigation support
 */

(function() {
  var toolsIndex = null;
  var selectedIndex = -1;
  var debounceTimer = null;
  
  // Load tools index
  function loadToolsIndex() {
    if (toolsIndex) return toolsIndex;
    
    // Check sessionStorage cache
    var cached = sessionStorage.getItem('tools-index');
    if (cached) {
      toolsIndex = JSON.parse(cached);
      return toolsIndex;
    }
    
    // Fetch from server
    return fetch('/tools-index.json')
      .then(function(response) {
        if (!response.ok) throw new Error('Failed to load tools index');
        return response.json();
      })
      .then(function(data) {
        toolsIndex = data;
        sessionStorage.setItem('tools-index', JSON.stringify(data));
        return data;
      })
      .catch(function(err) {
        console.error('Error loading tools index:', err);
        return [];
      });
  }
  
  // Search tools
  function searchTools(query) {
    if (!toolsIndex || !query) return [];
    
    query = query.toLowerCase().trim();
    if (query.length < 2) return [];
    
    var results = toolsIndex.filter(function(tool) {
      var nameMatch = tool.name.toLowerCase().indexOf(query) !== -1;
      var descMatch = tool.description.toLowerCase().indexOf(query) !== -1;
      var catMatch = tool.category.toLowerCase().indexOf(query) !== -1;
      var keywordMatch = tool.keywords.some(function(kw) {
        return kw.toLowerCase().indexOf(query) !== -1;
      });
      
      return nameMatch || descMatch || catMatch || keywordMatch;
    });
    
    return results.slice(0, 10); // Limit to 10 results
  }
  
  // Render search results
  function renderResults(results, container, input) {
    if (!container) return;
    
    if (results.length === 0) {
      container.innerHTML = '<div class="search-no-results">No tools found. Try "pdf", "image", or "password"</div>';
      container.classList.add('show');
      selectedIndex = -1;
      return;
    }
    
    var html = results.map(function(tool, index) {
      return '<div class="search-result-item" data-index="' + index + '" data-url="' + tool.url + '">' +
        '<div class="search-result-icon">' + tool.icon + '</div>' +
        '<div class="search-result-content">' +
          '<div class="search-result-name">' + tool.name + '</div>' +
          '<div class="search-result-category">' + tool.category + '</div>' +
        '</div>' +
      '</div>';
    }).join('');
    
    container.innerHTML = html;
    container.classList.add('show');
    selectedIndex = -1;
    
    // Add click handlers
    var items = container.querySelectorAll('.search-result-item');
    items.forEach(function(item) {
      item.addEventListener('click', function() {
        var url = item.getAttribute('data-url');
        if (url) {
          window.location.href = url;
        }
      });
    });
  }
  
  // Keyboard navigation
  function handleKeyboard(e, results, container, input) {
    if (!container.classList.contains('show')) return;
    
    var items = container.querySelectorAll('.search-result-item');
    if (items.length === 0) return;
    
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      updateSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, -1);
      updateSelection(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && items[selectedIndex]) {
        var url = items[selectedIndex].getAttribute('data-url');
        if (url) window.location.href = url;
      }
    } else if (e.key === 'Escape') {
      container.classList.remove('show');
      selectedIndex = -1;
    }
  }
  
  function updateSelection(items) {
    items.forEach(function(item, index) {
      item.classList.remove('selected');
      if (index === selectedIndex) {
        item.classList.add('selected');
      }
    });
  }
  
  // Initialize search
  function initSearch() {
    var searchInput = document.getElementById('tool-search');
    var searchResults = document.getElementById('search-results');
    
    if (!searchInput || !searchResults) return;
    
    // Load index on focus
    searchInput.addEventListener('focus', function() {
      loadToolsIndex();
    });
    
    // Search on input with debounce
    searchInput.addEventListener('input', function(e) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function() {
        var query = searchInput.value;
        var results = searchTools(query);
        renderResults(results, searchResults, searchInput);
      }, 150);
    });
    
    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
      handleKeyboard(e, [], searchResults, searchInput);
    });
    
    // Hide results on blur (with delay for click handling)
    searchInput.addEventListener('blur', function() {
      setTimeout(function() {
        searchResults.classList.remove('show');
      }, 200);
    });
  }
  
  // Initialize on DOM ready
  document.addEventListener('DOMContentLoaded', initSearch);
  
  // Expose for manual initialization
  window.initSearch = initSearch;
  window.loadToolsIndex = loadToolsIndex;
})();