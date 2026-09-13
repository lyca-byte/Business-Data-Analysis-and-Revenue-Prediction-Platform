/**
 * main.js
 * -------
 * Shared utilities loaded on every page.
 * - Active nav link highlighting
 * - Currency formatting helpers
 */

'use strict';

// ── Active navigation link ────────────────────────────────────────────────────
// Compares the current page filename to each nav link href and adds
// the 'active' class to the matching link.
(function setActiveNavLink() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const linkPage = link.getAttribute('href').split('/').pop();
    if (linkPage === currentPage) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
})();


// ── Shared formatting utilities ───────────────────────────────────────────────

/**
 * Format a number as USD currency.
 * formatCurrency(165608.96) → "$165,609"
 */
function formatCurrency(value, decimals = 0) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Format a number with thousand separators.
 * formatNumber(50000) → "50,000"
 */
function formatNumber(value, decimals = 0) {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Format a percentage value.
 * formatPercent(0.8847) → "88.47%"
 */
function formatPercent(value, decimals = 2) {
  return (value * 100).toFixed(decimals) + '%';
}
