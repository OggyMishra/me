// Theme toggle
(function () {
  const toggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  // Restore saved theme or default to dark
  const saved = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', saved);
  updateIcon(saved);

  if (toggle) {
    toggle.addEventListener('click', function () {
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateIcon(next);
    });
  }

  function updateIcon(theme) {
    if (!toggle) return;
    toggle.innerHTML = theme === 'dark'
      ? '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 12a4 4 0 100-8 4 4 0 000 8zm0 1.5a5.5 5.5 0 110-11 5.5 5.5 0 010 11zM8 0a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0V.75A.75.75 0 018 0zm0 12a.75.75 0 01.75.75v1.5a.75.75 0 01-1.5 0v-1.5A.75.75 0 018 12zm7-4a.75.75 0 01-.75.75h-1.5a.75.75 0 010-1.5h1.5A.75.75 0 0115 8zM4 8a.75.75 0 01-.75.75H1.75a.75.75 0 010-1.5h1.5A.75.75 0 014 8z"/></svg>'
      : '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M9.598 1.591a.75.75 0 01.785-.175 7 7 0 11-8.967 8.967.75.75 0 01.961-.96 5.5 5.5 0 007.046-7.046.75.75 0 01.175-.786z"/></svg>';
  }

  // Mobile menu toggle
  const menuBtn = document.getElementById('mobile-menu-btn');
  const nav = document.getElementById('main-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      nav.classList.toggle('open');
    });
    // Close on nav link click
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('open');
      });
    });
  }

  // Contribution graph (decorative, generate random data)
  const grid = document.getElementById('contrib-grid');
  if (grid) {
    var levels = ['', 'l1', 'l2', 'l3', 'l4'];
    // 52 weeks x 7 days
    for (var w = 0; w < 52; w++) {
      var col = document.createElement('div');
      col.className = 'contrib-col';
      for (var d = 0; d < 7; d++) {
        var cell = document.createElement('div');
        cell.className = 'contrib-cell';
        // Weighted random: most cells empty, some active
        var r = Math.random();
        if (r > 0.7) cell.classList.add(levels[Math.ceil(Math.random() * 4)]);
        col.appendChild(cell);
      }
      grid.appendChild(col);
    }
  }
})();
