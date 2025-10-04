(function ($) {
    if (!$) {
        return;
    }

    if (!$.expr[':'].Contains) {
        // custom css expression for a case-insensitive contains()
        $.expr[':'].Contains = function (element, index, match) {
            var text = element.textContent || element.innerText || '';
            return text.toUpperCase().indexOf(match[3].toUpperCase()) >= 0;
        };
    }

    function FilterList($input) {
        this.$input = $input;
        this.listSelector = $input.data('filterList') || '.list-of-tags';
        this.sectionTitleSelector = $input.data('filterSectionTitle') || '.tag-title';
        this.sectionListSelector = $input.data('filterSectionList') || '.list-articles-under-tag-category';
        this.$list = $(this.listSelector);
        this.$sectionTitles = $(this.sectionTitleSelector);
    }

    FilterList.prototype.showAllSections = function () {
        var sectionSelector = this.sectionListSelector;
        this.$sectionTitles.each(function () {
            var $title = $(this);
            $title.show();
            $title.next(sectionSelector).show();
        });
    };

    FilterList.prototype.hideAllSections = function () {
        var sectionSelector = this.sectionListSelector;
        this.$sectionTitles.each(function () {
            var $title = $(this);
            $title.hide();
            $title.next(sectionSelector).hide();
        });
    };

    FilterList.prototype.showSectionsByLinks = function ($links) {
        var ids = $links.map(function () {
            return $(this).attr('href');
        }).get();
        if (!ids.length) {
            this.hideAllSections();
            return;
        }
        var sectionSelector = this.sectionListSelector;
        this.$sectionTitles.each(function () {
            var $title = $(this);
            var anchor = '#' + this.id;
            var shouldShow = ids.indexOf(anchor) !== -1;
            $title.toggle(shouldShow);
            $title.next(sectionSelector).toggle(shouldShow);
        });
    };

    FilterList.prototype.filterList = function (term) {
        var $items = this.$list.find('li');
        if (!term) {
            $items.show();
            return;
        }
        var selector = 'a:Contains(' + term + ')';
        this.$list.find(selector).parent().show();
        this.$list.find('a').not(selector).parent().hide();
    };

    FilterList.prototype.filterView = function (term) {
        var value = term || '';
        this.showAllSections();
        this.filterList(value);
        if (!value) {
            return;
        }
        var $matches = this.$list.find('a:Contains(' + value + ')');
        if ($matches.length) {
            this.showSectionsByLinks($matches);
        } else {
            this.hideAllSections();
        }
    };

    FilterList.prototype.bindInput = function () {
        var self = this;
        this.$input.on('input', function () {
            self.filterView($(this).val());
        });
    };

    FilterList.prototype.bindListClick = function () {
        var self = this;
        this.$list.on('click', 'a', function (event) {
            var target = $(this).attr('href');
            var $targetTitle = $(target);
            if (!$targetTitle.length) {
                return;
            }
            event.preventDefault();
            self.$sectionTitles.not($targetTitle).hide().next(self.sectionListSelector).hide();
            $targetTitle.show();
            $targetTitle.next(self.sectionListSelector).show();
            if (typeof window !== 'undefined') {
                window.location.hash = target;
            }
        });
    };

    FilterList.prototype.init = function () {
        if (!this.$input.length || !this.$list.length || !this.$sectionTitles.length) {
            return;
        }
        this.bindInput();
        this.bindListClick();
        if (this.$input.val()) {
            this.filterView(this.$input.val());
        }
    };

    $(function () {
        $('input.filterinput[data-filter-list]').each(function () {
            var $input = $(this);
            if ($input.data('filterBound')) {
                return;
            }
            $input.data('filterBound', true);
            var filter = new FilterList($input);
            filter.init();
        });
    });
}(window.jQuery));
