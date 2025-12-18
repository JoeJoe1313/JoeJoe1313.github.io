(function () {
    var overlay = document.getElementById('zoom-overlay');
    if (!overlay) {
        return;
    }

    var overlayMedia = overlay.querySelector('.zoom-overlay__media');
    if (!overlayMedia) {
        return;
    }

    var closeBtn = overlay.querySelector('.zoom-overlay__close');
    var mermaidRenderToken = 0;
    var activeResizeHandler = null;

    function clearActiveResizeHandler() {
        if (!activeResizeHandler) {
            return;
        }
        window.removeEventListener('resize', activeResizeHandler);
        activeResizeHandler = null;
    }

    function setActiveResizeHandler(handler) {
        clearActiveResizeHandler();
        activeResizeHandler = handler;
        window.addEventListener('resize', activeResizeHandler);
    }

    function getOverlayAvailableBox() {
        var rect = overlay.getBoundingClientRect();
        var styles = window.getComputedStyle(overlay);
        var padLeft = parseFloat(styles.paddingLeft) || 0;
        var padRight = parseFloat(styles.paddingRight) || 0;
        var padTop = parseFloat(styles.paddingTop) || 0;
        var padBottom = parseFloat(styles.paddingBottom) || 0;

        var maxWidth = Math.min(rect.width - padLeft - padRight, 1600, window.innerWidth * 0.96);
        var maxHeight = Math.min(rect.height - padTop - padBottom, window.innerHeight * 0.95);

        return {
            width: Math.max(0, maxWidth),
            height: Math.max(0, maxHeight)
        };
    }

    function getSvgViewBox(svg) {
        if (svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width && svg.viewBox.baseVal.height) {
            return {
                width: svg.viewBox.baseVal.width,
                height: svg.viewBox.baseVal.height
            };
        }

        var viewBox = svg.getAttribute('viewBox');
        if (!viewBox) {
            return null;
        }

        var parts = viewBox.trim().split(/\s+|,/).map(Number);
        if (parts.length !== 4 || parts.some(function (n) { return !Number.isFinite(n); })) {
            return null;
        }

        return { width: parts[2], height: parts[3] };
    }

    function fitSvgToViewport(svg) {
        var viewBox = getSvgViewBox(svg);
        if (!viewBox) {
            return;
        }

        var available = getOverlayAvailableBox();
        if (available.width <= 0 || available.height <= 0) {
            return;
        }

        var aspect = viewBox.width / viewBox.height;
        if (!Number.isFinite(aspect) || aspect <= 0) {
            return;
        }

        var width = available.width;
        var height = width / aspect;
        if (height > available.height) {
            height = available.height;
            width = height * aspect;
        }

        svg.removeAttribute('width');
        svg.removeAttribute('height');
        svg.style.width = Math.floor(width) + 'px';
        svg.style.height = Math.floor(height) + 'px';
        svg.style.maxWidth = 'none';
        svg.style.maxHeight = 'none';
    }

    function openOverlayShell(isSvg) {
        overlay.classList.toggle('is-svg', Boolean(isSvg));
        overlay.classList.add('is-open');
        overlay.setAttribute('aria-hidden', 'false');
        overlayMedia.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        closeBtn.focus();
    }

    function openOverlay(img) {
        clearActiveResizeHandler();
        var zoomSrc = img.dataset.zoomSrc || img.src;
        var srcWithoutQuery = zoomSrc.split(/[?#]/)[0];
        var isSvg = /\.svg$/i.test(srcWithoutQuery);
        var isTransparentPng = /\.png$/i.test(srcWithoutQuery) && img.classList.contains('zoomable--transparent');

        overlayMedia.textContent = '';
        var overlayImg = document.createElement('img');
        overlayImg.src = zoomSrc;
        overlayImg.alt = img.alt || '';
        overlayMedia.appendChild(overlayImg);
        openOverlayShell(isSvg || isTransparentPng);
    }

    function getMermaidAlt(mermaidEl) {
        var figure = mermaidEl.closest && mermaidEl.closest('figure');
        if (!figure) {
            return 'Diagram';
        }

        var caption = figure.querySelector('figcaption');
        if (!caption) {
            return 'Diagram';
        }

        return (caption.textContent || '').trim() || 'Diagram';
    }

    function openMermaidOverlay(mermaidEl) {
        clearActiveResizeHandler();
        var source = mermaidEl.dataset.mermaidSrc;
        var mermaid = window.mermaid;

        mermaidRenderToken += 1;
        var token = mermaidRenderToken;

        overlayMedia.textContent = 'Loading diagram…';
        openOverlayShell(true);

        if (!mermaid || !source) {
            var existingSvg = mermaidEl.querySelector('svg');
            if (!existingSvg) {
                overlayMedia.textContent = 'Unable to zoom diagram.';
                return;
            }

            overlayMedia.textContent = '';
            var clonedSvg = existingSvg.cloneNode(true);
            overlayMedia.appendChild(clonedSvg);
            fitSvgToViewport(clonedSvg);
            setActiveResizeHandler(function () {
                if (token !== mermaidRenderToken || !overlay.classList.contains('is-open')) {
                    return;
                }
                fitSvgToViewport(clonedSvg);
            });
            return;
        }

        var renderId = 'zoom-diagram-' + Math.random().toString(36).slice(2);
        Promise.resolve(mermaid.render(renderId, source)).then(function (result) {
            if (token !== mermaidRenderToken || !overlay.classList.contains('is-open')) {
                return;
            }

            var svgCode = result && result.svg ? result.svg : result;
            if (!svgCode || typeof svgCode !== 'string') {
                overlayMedia.textContent = 'Unable to render diagram.';
                return;
            }

            overlayMedia.innerHTML = svgCode;
            if (typeof result.bindFunctions === 'function') {
                result.bindFunctions(overlayMedia);
            }

            var renderedSvg = overlayMedia.querySelector('svg');
            if (renderedSvg && !renderedSvg.getAttribute('aria-label')) {
                renderedSvg.setAttribute('aria-label', getMermaidAlt(mermaidEl));
            }
            if (renderedSvg && !renderedSvg.getAttribute('preserveAspectRatio')) {
                renderedSvg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
            }
            if (renderedSvg) {
                fitSvgToViewport(renderedSvg);
                setActiveResizeHandler(function () {
                    if (token !== mermaidRenderToken || !overlay.classList.contains('is-open')) {
                        return;
                    }
                    fitSvgToViewport(renderedSvg);
                });
            }
        }).catch(function () {
            if (token !== mermaidRenderToken || !overlay.classList.contains('is-open')) {
                return;
            }
            overlayMedia.textContent = 'Unable to render diagram.';
        });
    }

    function closeOverlay() {
        mermaidRenderToken += 1;
        clearActiveResizeHandler();
        overlay.classList.remove('is-open');
        overlay.setAttribute('aria-hidden', 'true');
        overlay.classList.remove('is-svg');
        overlayMedia.textContent = '';
        overlayMedia.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    document.querySelectorAll('.article-content img.zoomable').forEach(function (img) {
        img.addEventListener('click', function () {
            openOverlay(img);
        });
    });

    document.querySelectorAll('.article-content pre.mermaid').forEach(function (diagram) {
        if (!diagram.dataset.mermaidSrc && !diagram.querySelector('svg')) {
            diagram.dataset.mermaidSrc = (diagram.textContent || '').trim();
        }

        diagram.setAttribute('tabindex', '0');
        diagram.setAttribute('role', 'button');
        if (!diagram.getAttribute('aria-label')) {
            diagram.setAttribute('aria-label', 'Zoom diagram');
        }

        diagram.addEventListener('click', function (event) {
            if (event.target && event.target.closest && event.target.closest('a')) {
                return;
            }
            openMermaidOverlay(diagram);
        });

        diagram.addEventListener('keydown', function (event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                openMermaidOverlay(diagram);
            }
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
