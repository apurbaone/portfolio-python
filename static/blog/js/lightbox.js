// Minimal lightbox (dependency-free). Attaches to elements with .lightbox-trigger
(function(){
  function qs(sel, ctx){ return (ctx||document).querySelector(sel); }
  function qsa(sel, ctx){ return Array.from((ctx||document).querySelectorAll(sel)); }

  document.addEventListener('DOMContentLoaded', function(){
    var lb = qs('#lightbox');
    if(!lb) return;
    var imgEl = qs('.lightbox-image', lb);
    var capEl = qs('.lightbox-caption', lb);
    var closeBtn = qs('.lightbox-close', lb);

    function open(src, alt){
      imgEl.src = src;
      imgEl.alt = alt || '';
      capEl.textContent = alt || '';
      lb.setAttribute('aria-hidden','false');
      document.body.style.overflow = 'hidden';
    }
    function close(){
      lb.setAttribute('aria-hidden','true');
      imgEl.src = '#';
      capEl.textContent = '';
      document.body.style.overflow = '';
    }

    qsa('.lightbox-trigger').forEach(function(a){
      a.addEventListener('click', function(e){
        e.preventDefault();
        var src = a.getAttribute('href') || a.dataset.src;
        var caption = a.dataset.caption || a.getAttribute('title') || '';
        open(src, caption);
      });
    });

    closeBtn.addEventListener('click', close);
    lb.addEventListener('click', function(e){ if(e.target===lb) close(); });
    document.addEventListener('keyup', function(e){ if(e.key==='Escape') close(); });
  });
})();
