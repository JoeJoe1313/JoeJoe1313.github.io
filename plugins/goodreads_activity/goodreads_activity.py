from __future__ import unicode_literals

import logging

from pelican import signals

logger = logging.getLogger(__name__)

_activity_loader = None


class GoodreadsActivity:
    def __init__(self, settings):
        import feedparser

        self.activities = {}
        activity_feeds = settings["GOODREADS_ACTIVITY_FEED"]
        for shelf, url in activity_feeds.items():
            self.activities[shelf] = feedparser.parse(url)

    def fetch(self):
        goodreads_activity = {}
        for shelf, parsed in self.activities.items():
            goodreads_activity[shelf] = {
                "shelf_title": " ".join(word.capitalize() for word in shelf.split("_")),
                "books": [],
            }
            for entry in parsed["entries"]:
                book = {
                    "title": entry.title,
                    "author": entry.author_name,
                    "link": entry.link,
                    "l_cover": entry.book_large_image_url,
                    "m_cover": entry.book_medium_image_url,
                    "s_cover": entry.book_small_image_url,
                    "description": entry.book_description,
                    "rating": entry.user_rating,
                    "review": entry.user_review,
                    "tags": entry.user_shelves,
                }
                goodreads_activity[shelf]["books"].append(book)

        return goodreads_activity


def _get_loader(settings):
    global _activity_loader

    if "GOODREADS_ACTIVITY_FEED" not in settings:
        return None

    if _activity_loader is None:
        try:
            _activity_loader = GoodreadsActivity(settings)
        except ImportError:
            logger.warning(
                "`goodreads_activity` failed to load dependency `feedparser`."
                " `goodreads_activity` plugin not loaded."
            )
            return None

    return _activity_loader


def fetch_goodreads_activity(gen, metadata):
    loader = _get_loader(gen.settings)
    if loader is not None:
        gen.context["goodreads_activity"] = loader.fetch()


def add_to_jinja_globals(pelican_obj):
    loader = _get_loader(pelican_obj.settings)
    if loader is None:
        return

    jinja_globals = pelican_obj.settings.setdefault("JINJA_GLOBALS", {})
    jinja_globals["goodreads_activity"] = loader.fetch()
    if "GOODREADS_ACTIVITY_FEED" in pelican_obj.settings:
        jinja_globals["GOODREADS_ACTIVITY_FEED"] = pelican_obj.settings[
            "GOODREADS_ACTIVITY_FEED"
        ]


def register():
    signals.initialized.connect(add_to_jinja_globals)
    signals.article_generator_context.connect(fetch_goodreads_activity)
    signals.page_generator_context.connect(fetch_goodreads_activity)
