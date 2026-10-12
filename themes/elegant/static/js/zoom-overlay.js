(function () {
    var overlay = document.getElementById('zoom-overlay');
    if (!overlay) {
        return;
    }

    var viewport = overlay.querySelector('.zoom-overlay__viewport');
    var media = overlay.querySelector('.zoom-overlay__media');
    var caption = overlay.querySelector('.zoom-overlay__caption');
    var closeBtn = overlay.querySelector('.zoom-overlay__close');
    var zoomBtn = overlay.querySelector('.zoom-overlay__toggle');
    var renderToken = 0;
    var activeMedia = null;
    var mediaSize = null;
    var zoomed = false;
    var opener = null;
    var previousOverflow = '';

    function getCaption(element) {
        var figure = element.closest('figure');
        var figcaption = figure && figure.querySelector('figcaption');
        return figcaption ? figcaption.textContent.trim() : (element.alt || '');
    }

    function fitMedia() {
        if (!activeMedia || !mediaSize || !overlay.open) {
            return;
        }
        // Measure the viewport, including space reserved for controls and the caption.
        // offsetWidth stays stable when magnification introduces scrollbars.
        var scale = Math.min(Math.min(viewport.offsetWidth, 1600) / mediaSize.width,
            viewport.offsetHeight / mediaSize.height);
        if (!mediaSize.vector) {
            scale = Math.min(scale, 1);
        }
        scale *= zoomed ? 2 : 1;
        activeMedia.style.width = Math.floor(mediaSize.width * scale) + 'px';
        activeMedia.style.height = Math.floor(mediaSize.height * scale) + 'px';
        activeMedia.style.maxWidth = 'none';
        activeMedia.style.maxHeight = 'none';
    }

    function setMedia(element, width, height, vector) {
        if (!(width > 0 && height > 0)) {
            showMessage('Unable to determine the image size.');
            return;
        }
        activeMedia = element;
        mediaSize = { width: width, height: height, vector: vector };
        media.replaceChildren(element);
        zoomBtn.disabled = false;
        fitMedia();
    }

    function showMessage(message) {
        activeMedia = null;
        mediaSize = null;
        zoomBtn.disabled = true;
        var status = document.createElement('p');
        status.setAttribute('role', 'status');
        status.textContent = message;
        media.replaceChildren(status);
    }

    function openShell(element, isSvg, message) {
        renderToken += 1;
        zoomed = false;
        zoomBtn.textContent = 'Zoom in (2×)';
        showMessage(message);
        caption.textContent = getCaption(element);
        overlay.classList.toggle('is-svg', isSvg);
        if (!overlay.open) {
            opener = element.closest('a') || element;
            previousOverflow = document.body.style.overflow;
            document.body.style.overflow = 'hidden';
            overlay.showModal();
        }
        viewport.scrollTo(0, 0);
        closeBtn.focus();
        return renderToken;
    }

    function isCurrent(token) {
        return token === renderToken && overlay.open;
    }

    function openImage(img) {
        var src = img.dataset.zoomSrc || img.currentSrc || img.src;
        var isSvg = /\.svg(?:[?#]|$)/i.test(src) || /^data:image\/svg\+xml/i.test(src);
        var whiteBackground = isSvg || img.classList.contains('zoomable--transparent');
        var token = openShell(img, whiteBackground, 'Loading image…');
        var enlarged = new Image();
        enlarged.alt = img.alt || '';
        enlarged.onload = function () {
            if (isCurrent(token)) {
                setMedia(enlarged, enlarged.naturalWidth, enlarged.naturalHeight, isSvg);
            }
        };
        enlarged.onerror = function () {
            if (isCurrent(token)) {
                showMessage('Unable to load this image. Close the viewer and try again.');
            }
        };
        enlarged.src = src;
    }

    function setSvg(svg, description) {
        var box = svg.viewBox && svg.viewBox.baseVal;
        if (!box || !(box.width > 0 && box.height > 0)) {
            showMessage('Unable to determine the diagram size.');
            return;
        }
        svg.setAttribute('role', 'img');
        if (!svg.getAttribute('aria-label')) {
            svg.setAttribute('aria-label', description || 'Diagram');
        }
        svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        svg.removeAttribute('width');
        svg.removeAttribute('height');
        setMedia(svg, box.width, box.height, true);
    }

    function openMermaid(diagram) {
        var source = diagram.dataset.mermaidSrc;
        var mermaid = window.mermaid;
        var token = openShell(diagram, true, 'Loading diagram…');
        if (!mermaid || !source) {
            var existing = diagram.querySelector('svg');
            if (existing) {
                setSvg(existing.cloneNode(true), getCaption(diagram));
            } else {
                showMessage('Unable to zoom this diagram.');
            }
            return;
        }

        // Starting in a promise also catches synchronous render failures.
        Promise.resolve().then(function () {
            return mermaid.render('zoom-diagram-' + token, source);
        }).then(function (result) {
            if (!isCurrent(token)) {
                return;
            }
            var svgCode = result && result.svg ? result.svg : result;
            if (typeof svgCode !== 'string') {
                showMessage('Unable to render this diagram.');
                return;
            }
            media.innerHTML = svgCode;
            var svg = media.querySelector('svg');
            if (!svg) {
                showMessage('Unable to render this diagram.');
                return;
            }
            setSvg(svg, getCaption(diagram));
            if (typeof result.bindFunctions === 'function') {
                result.bindFunctions(media);
            }
        }).catch(function () {
            if (isCurrent(token)) {
                showMessage('Unable to render this diagram.');
            }
        });
    }

    function closeOverlay() {
        if (!overlay.open) {
            return;
        }
        renderToken += 1;
        overlay.close();
        activeMedia = null;
        mediaSize = null;
        media.replaceChildren();
        document.body.style.overflow = previousOverflow;
        if (opener && opener.isConnected) {
            opener.focus({ preventScroll: true });
        }
        opener = null;
    }

    function makeTrigger(element, label, open) {
        element.setAttribute('tabindex', '0');
        element.setAttribute('role', 'button');
        element.setAttribute('aria-haspopup', 'dialog');
        element.setAttribute('aria-controls', 'zoom-overlay');
        if (!element.getAttribute('aria-label')) {
            element.setAttribute('aria-label', label);
        }
        element.addEventListener('click', function (event) {
            // Keep links inside Mermaid diagrams usable.
            if (event.target.closest('a') && event.target.closest('a') !== element) {
                return;
            }
            event.preventDefault();
            open();
        });
        element.addEventListener('keydown', function (event) {
            if (event.target !== element) {
                return;
            }
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                open();
            }
        });
    }

    document.querySelectorAll('.article-content img.zoomable').forEach(function (img) {
        makeTrigger(img.closest('a') || img, 'Zoom image: ' + (img.alt || 'Figure'), function () {
            openImage(img);
        });
    });
    document.querySelectorAll('.article-content pre.mermaid').forEach(function (diagram) {
        if (!diagram.dataset.mermaidSrc && !diagram.querySelector('svg')) {
            diagram.dataset.mermaidSrc = diagram.textContent.trim();
        }
        makeTrigger(diagram, 'Zoom diagram', function () {
            openMermaid(diagram);
        });
    });

    zoomBtn.addEventListener('click', function () {
        zoomed = !zoomed;
        zoomBtn.textContent = zoomed ? 'Fit to screen' : 'Zoom in (2×)';
        fitMedia();
        // Start at the center; the viewport supports touch, mouse and keyboard scrolling.
        viewport.scrollTo((viewport.scrollWidth - viewport.clientWidth) / 2,
            (viewport.scrollHeight - viewport.clientHeight) / 2);
    });
    closeBtn.addEventListener('click', closeOverlay);
    overlay.addEventListener('cancel', function (event) {
        event.preventDefault();
        closeOverlay();
    });
    overlay.addEventListener('click', function (event) {
        if (event.target === overlay || event.target === viewport || event.target === media) {
            closeOverlay();
        }
    });
    window.addEventListener('resize', fitMedia);
}());
