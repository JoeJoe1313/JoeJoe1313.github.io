(function () {
    var overlay = document.getElementById('zoom-overlay');
    if (!overlay) {
        return;
    }

    var overlayImg = overlay.querySelector('img');
    var closeBtn = overlay.querySelector('.zoom-overlay__close');

    function openOverlay(img) {
        overlayImg.src = img.dataset.zoomSrc || img.src;
        overlayImg.alt = img.alt || '';
        overlay.classList.add('is-open');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        closeBtn.focus();
    }

    function closeOverlay() {
        overlay.classList.remove('is-open');
        overlay.setAttribute('aria-hidden', 'true');
        overlayImg.src = '';
        document.body.style.overflow = '';
    }

    document.querySelectorAll('.article-content img.zoomable').forEach(function (img) {
        img.addEventListener('click', function () {
            openOverlay(img);
        });
    });

    overlay.addEventListener('click', function (event) {
        if (event.target === overlay) {
            closeOverlay();
        }
    });
    closeBtn.addEventListener('click', closeOverlay);
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && overlay.classList.contains('is-open')) {
            closeOverlay();
        }
    });
}());
