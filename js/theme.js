/**
 * Global Theme and Utility Functions
 * - Dark mode toggle with localStorage persistence
 * - Toast notification component
 * - Copy to clipboard with feedback
 */

(function() {
  // =====================
  // Theme Management
  // =====================
  
  function initTheme() {
    var savedTheme = localStorage.getItem('theme');
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    
    updateThemeIcon();
  }
  
  function toggleTheme() {
    var currentTheme = document.documentElement.getAttribute('data-theme');
    
    if (currentTheme === 'dark') {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    }
    
    updateThemeIcon();
  }
  
  function updateThemeIcon() {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    var toggleBtn = document.querySelector('.theme-toggle');
    
    if (toggleBtn) {
      toggleBtn.innerHTML = isDark ? '☀️' : '🌙';
      toggleBtn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    }
  }
  
  // Initialize theme on page load
  initTheme();
  
  // Listen for system theme changes
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
      if (!localStorage.getItem('theme')) {
        if (e.matches) {
          document.documentElement.setAttribute('data-theme', 'dark');
        } else {
          document.documentElement.removeAttribute('data-theme');
        }
        updateThemeIcon();
      }
    });
  }
  
  // =====================
  // Toast Component
  // =====================
  
  var toastContainer = null;
  
  function createToastContainer() {
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'toast-container';
      toastContainer.id = 'toast-container';
      document.body.appendChild(toastContainer);
    }
    return toastContainer;
  }
  
  function showToast(message, duration) {
    duration = duration || 2000;
    
    var container = createToastContainer();
    var toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Trigger animation
    setTimeout(function() {
      toast.classList.add('show');
    }, 10);
    
    // Remove after duration
    setTimeout(function() {
      toast.classList.remove('show');
      setTimeout(function() {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, duration);
  }
  
  // =====================
  // Copy to Clipboard
  // =====================
  
  function copyToClipboard(text, buttonElement) {
    var success = false;
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!');
        if (buttonElement) {
          var original = buttonElement.textContent || buttonElement.innerText;
          buttonElement.textContent = 'Copied!';
          buttonElement.disabled = true;
          setTimeout(function() {
            buttonElement.textContent = original;
            buttonElement.disabled = false;
          }, 2000);
        }
        success = true;
      }).catch(function(err) {
        fallbackCopy(text, buttonElement);
      });
    } else {
      fallbackCopy(text, buttonElement);
    }
    
    return success;
  }
  
  function fallbackCopy(text, buttonElement) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '0';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    
    try {
      document.execCommand('copy');
      showToast('Copied to clipboard!');
      if (buttonElement) {
        var original = buttonElement.textContent || buttonElement.innerText;
        buttonElement.textContent = 'Copied!';
        setTimeout(function() {
          buttonElement.textContent = original;
        }, 2000);
      }
    } catch (err) {
      showToast('Copy failed - please copy manually');
    }
    
    document.body.removeChild(textarea);
  }
  
  // =====================
  // Expose Global Functions
  // =====================
  
  window.toggleTheme = toggleTheme;
  window.showToast = showToast;
  window.copyToClipboard = copyToClipboard;
  
  // =====================
  // Setup Theme Toggle Button
  // =====================
  
  document.addEventListener('DOMContentLoaded', function() {
    var toggleBtn = document.querySelector('.theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
    }
    
    // Also setup nav toggle for mobile
    var navToggle = document.querySelector('.nav-toggle');
    var navLinks = document.querySelector('.nav-links');
    if (navToggle && navLinks) {
      navToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', navLinks.classList.contains('active'));
      });
    }
  });
})();