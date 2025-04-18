from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)

from pelican import signals


class GoodreadsActivity:
    def __init__(self, generator):
        import feedparser

        self.activities = dict()
        activity_feeds = generator.settings["GOODREADS_ACTIVITY_FEED"]
        for activity_feed in activity_feeds:
            self.activities[activity_feed] = feedparser.parse(
                activity_feeds[activity_feed]
            )

    def fetch(self):
        goodreads_activity = dict()
        for activity_feed in self.activities:
            goodreads_activity[activity_feed] = {
                # "shelf_title": self.activities[activity_feed]["feed"]["title"],
                "shelf_title": " ".join(
                    word.capitalize() for word in activity_feed.split("_")
                ),
                "books": [],
            }
            for entry in self.activities[activity_feed]["entries"]:
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
                goodreads_activity[activity_feed]["books"].append(book)

        return goodreads_activity


def fetch_goodreads_activity(gen, metadata):
    if "GOODREADS_ACTIVITY_FEED" in gen.settings:
        gen.context["goodreads_activity"] = gen.goodreads_activity.fetch()


def initialize_feedparser(generator):
    generator.goodreads_activity = GoodreadsActivity(generator)


def register():
    try:
        signals.article_generator_init.connect(initialize_feedparser)
        signals.article_generator_context.connect(fetch_goodreads_activity)
    except ImportError:
        logger.warning(
            "`goodreads_activity` failed to load dependency `feedparser`."
            "`goodreads_activity` plugin not loaded."
        )
