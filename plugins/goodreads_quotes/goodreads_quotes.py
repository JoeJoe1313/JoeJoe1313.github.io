from __future__ import unicode_literals

import logging

from pelican import signals

logger = logging.getLogger(__name__)

_quotes_loader = None


class GoodreadsQuotes:
    def __init__(self, settings):
        import feedparser

        self.feed = feedparser.parse(settings["GOODREADS_QUOTES"])

    def fetch(self):
        goodreads_quotes = {"shelf_title": "Quotes", "quotes": []}
        for entry in self.feed["entries"]:
            try:
                content, author = entry["summary"].split(" -- ", 1)
            except ValueError:
                content, author = entry["summary"], ""
            quote = {
                "id": entry["id"],
                "published": entry["published_parsed"],
                "title": entry["title"],
                "quote": content,
                "author": ("-- " + author) if author else "",
            }
            goodreads_quotes["quotes"].append(quote)

        return goodreads_quotes


def _get_loader(settings):
    global _quotes_loader

    if "GOODREADS_QUOTES" not in settings:
        return None

    if _quotes_loader is None:
        try:
            _quotes_loader = GoodreadsQuotes(settings)
        except ImportError:
            logger.warning(
                "`goodreads_quotes` failed to load dependency `feedparser`."
                " `goodreads_quotes` plugin not loaded."
            )
            return None

    return _quotes_loader


def fetch_goodreads_quotes(gen, metadata):
    loader = _get_loader(gen.settings)
    if loader is not None:
        gen.context["goodreads_quotes"] = loader.fetch()


def add_to_jinja_globals(pelican_obj):
    loader = _get_loader(pelican_obj.settings)
    if loader is None:
        return

    jinja_globals = pelican_obj.settings.setdefault("JINJA_GLOBALS", {})
    jinja_globals["goodreads_quotes"] = loader.fetch()


def register():
    signals.initialized.connect(add_to_jinja_globals)
    signals.article_generator_context.connect(fetch_goodreads_quotes)
    signals.page_generator_context.connect(fetch_goodreads_quotes)
