from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)

from pelican import signals


class GoodreadsQuotes:
    def __init__(self, generator):
        import feedparser

        self.quotes = feedparser.parse(generator.settings["GOODREADS_QUOTES"])

    def fetch(self):
        goodreads_quotes = {"shelf_title": "Quotes", "quotes": []}
        for entry in self.quotes["entries"]:
            content, author = entry["summary"].split(" -- ", 1)
            quote = {
                "id": entry["id"],
                "published": entry["published_parsed"],
                "title": entry["title"],
                "quote": content,
                "author": "-- " + author,
            }
            goodreads_quotes["quotes"].append(quote)

        return goodreads_quotes


def fetch_goodreads_quotes(gen, metadata):
    if "GOODREADS_QUOTES" in gen.settings:
        gen.context["goodreads_quotes"] = gen.goodreads_quotes.fetch()


def initialize_feedparser(generator):
    generator.goodreads_quotes = GoodreadsQuotes(generator)


def register():
    try:
        signals.article_generator_init.connect(initialize_feedparser)
        signals.article_generator_context.connect(fetch_goodreads_quotes)
    except ImportError:
        logger.warning(
            "`goodreads_quotes` failed to load dependency `feedparser`."
            "`goodreads_quotes` plugin not loaded."
        )
