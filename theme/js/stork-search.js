(function (global) {
    "use strict";

    function escapeHtml(value) {
        return value.replace(/[&<>"']/g, function (character) {
            return {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#39;"
            }[character];
        });
    }

    function syncHeading(selector, term) {
        var heading = document.querySelector(selector);
        if (!heading) {
            return;
        }

        var message = heading.querySelector('[data-stork-current-term]');
        var trimmed = term.trim();

        if (trimmed) {
            if (!message) {
                message = document.createElement('p');
                message.setAttribute('data-stork-current-term', '');
                heading.appendChild(message);
            }
            message.innerHTML = 'Showing matches for <code>' + escapeHtml(trimmed) + '</code>';
        } else if (message) {
            heading.removeChild(message);
        }
    }

    function updateQueryString(param, value) {
        if (!global.history || !global.history.replaceState) {
            return;
        }
        var url = new URL(global.location.href);
        if (value) {
            url.searchParams.set(param, value);
        } else {
            url.searchParams.delete(param);
        }
        global.history.replaceState({}, '', url);
    }

    function triggerInput(element) {
        if (!element) {
            return;
        }

        var event;
        if (typeof Event === 'function') {
            event = new Event('input', { bubbles: true });
        } else {
            event = document.createEvent('Event');
            event.initEvent('input', true, true);
        }

        element.dispatchEvent(event);
    }

    function initializeStorkSearch(config) {
        if (!global.stork || typeof global.stork.register !== 'function') {
            console.error('Stork search runtime is required but was not loaded.');
            return Promise.reject(new Error('stork runtime missing'));
        }

        if (!global.__storkInitialized && typeof global.stork.initialize === 'function') {
            global.stork.initialize();
            global.__storkInitialized = true;
        }

        var indexName = config.index || 'site-search';
        var indexUrl = config.indexUrl || 'search-index.st';
        var inputSelector = config.inputSelector || "[data-stork='" + indexName + "']";
        var resultSelector = config.outputSelector || "[data-stork='" + indexName + "-output']";
        var headingSelector = config.headingSelector || '#lunr-search-result-heading';
        var queryParam = config.queryParam || 'q';

        var input = document.querySelector(inputSelector);
        var output = document.querySelector(resultSelector);

        if (!input || !output) {
            return global.stork.register(indexName, indexUrl);
        }

        var params = new URLSearchParams(global.location.search);
        var initialTerm = (params.get(queryParam) || '').trim();

        // Handle real-time search and URL updates
        input.addEventListener('input', function () {
            var currentTerm = input.value.trim();
            syncHeading(headingSelector, currentTerm);
            updateQueryString(queryParam, currentTerm);
        });

        // Register and attach Stork
        var registrationPromise = global.stork.register(indexName, indexUrl);
        var readyPromise = registrationPromise.then(function () {
            if (typeof global.stork.attach === 'function') {
                var attachResult = global.stork.attach(indexName);
                if (attachResult && typeof attachResult.then === 'function') {
                    return attachResult;
                }
            }
            return undefined;
        });

        // Handle form submission (just prevent default and update URL)
        var form = input.form;
        if (form) {
            form.addEventListener('submit', function (event) {
                event.preventDefault();
                var term = input.value.trim();
                syncHeading(headingSelector, term);
                updateQueryString(queryParam, term);
            });
        }

        // Initialize with URL parameter if present
        return readyPromise.then(function () {
            if (initialTerm) {
                input.value = initialTerm;
                syncHeading(headingSelector, initialTerm);
                triggerInput(input);
            }
        });
    }

    global.initializeStorkSearch = initializeStorkSearch;
})(window);
