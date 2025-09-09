document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.querySelector('.hamburger');
  const leftNav = document.querySelector('.left-nav');
  const overlay = document.querySelector('.nav-overlay');
  const navLinks = document.querySelectorAll('.left-nav .nav a');

  if (!hamburger || !leftNav) return;

  function openNav() {
    leftNav.classList.add('open');
    overlay.classList.add('show');
  hamburger.setAttribute('aria-expanded', 'true');
  hamburger.classList.add('is-open');
  }
  function closeNav() {
    leftNav.classList.remove('open');
    overlay.classList.remove('show');
  hamburger.setAttribute('aria-expanded', 'false');
  hamburger.classList.remove('is-open');
  }

  hamburger.addEventListener('click', function () {
    if (leftNav.classList.contains('open')) closeNav(); else openNav();
  });

  overlay.addEventListener('click', closeNav);

  navLinks.forEach(a => a.addEventListener('click', (ev) => {
    const href = a.getAttribute('href');
    // Close nav immediately for all clicks so UX feels snappy
    closeNav();

    // If internal anchor, intercept and smooth-scroll
    if (href && href.startsWith('#')) {
      ev.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const headerOffset = 56; // mobile header height
        const elementPosition = target.getBoundingClientRect().top + window.pageYOffset;
        const offsetPosition = elementPosition - headerOffset - 12;
        window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
      }
      return;
    }

    // For same-origin page links (like /blog/) let browser navigate but ensure menu closed first.
    // If the link points to the current page + hash, force navigation after a short delay to allow close animation.
    if (href && (href === window.location.pathname || href === window.location.pathname + '/')) {
      // allow default behavior (or reassign to force reload)
      setTimeout(() => { window.location.href = href; }, 160);
    }
  }));

  // close on Escape
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNav(); });
});
