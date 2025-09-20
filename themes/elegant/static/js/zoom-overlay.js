(function () {
    var overlay = document.getElementById('zoom-overlay');
    if (!overlay) {
        return;
    }

    var overlayImg = overlay.querySelector('img');
    var closeBtn = overlay.querySelector('.zoom-overlay__close');

    function openOverlay(img) {
        var zoomSrc = img.dataset.zoomSrc || img.src;
        overlayImg.src = zoomSrc;
        overlayImg.alt = img.alt || '';

        var srcWithoutQuery = zoomSrc.split(/[?#]/)[0];
        var isSvg = /\.svg$/i.test(srcWithoutQuery);
        var isTransparentPng = /\.png$/i.test(srcWithoutQuery) && img.classList.contains('zoomable--transparent');
        overlay.classList.toggle('is-svg', isSvg || isTransparentPng);
        overlay.classList.add('is-open');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        closeBtn.focus();
    }

    function closeOverlay() {
        overlay.classList.remove('is-open');
        overlay.setAttribute('aria-hidden', 'true');
        overlay.classList.remove('is-svg');
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
