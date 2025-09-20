# AUTHOR = "Joana"
SITENAME = "JoJo's Blog"
SITEURL = ""

PATH = "content"
ARTICLE_PATHS = ["articles"]
PAGE_PATHS = ["pages"]
PAGE_SAVE_AS = "{slug}.html"
PAGE_URL = "{slug}.html"
OUTPUT_PATH = "docs"
TAGS_SAVE_AS = "tags.html"
ARTICLE_SAVE_AS = "{slug}.html"
AUTHORS_SAVE_AS = ""  # Prevent authors page from being generated
# CATEGORIES_SAVE_AS = ""  # Prevent category page from being generated
AUTHOR_SAVE_AS = ""
# TAG_SAVE_AS = ""
# TAG_URL = ""
# CATEGORY_SAVE_AS = ""
# ARCHIVES_SAVE_AS = ""
THEME = "themes/elegant"
STATIC_PATHS = [
    "theme/images",
    "images",
    "code",
]

TIMEZONE = "Europe/Sofia"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("GitHub", "https://github.com/JoeJoe1313"),
    # ("Pelican", "https://getpelican.com/"),
    # ("Python.org", "https://www.python.org/"),
    # ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    # ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("GitHub", "https://github.com/JoeJoe1313"),
    ("LinkedIn", "https://www.linkedin.com/in/joana-levtcheva-479844164/"),
    ("Twitter", "https://x.com/13_jo_jo_13"),
)
SOCIAL_PROFILE_LABEL = "Stay in Touch"

DEFAULT_PAGINATION = 5
READING_TIME_LOWER_LIMIT = 1

PLUGINS = [
    "plugins.summary",
    "plugins.render_math",
    "plugins.liquid_tags.include_code",
    "plugins.liquid_tags.include_code_collapsible",
    "plugins.goodreads_activity",
    "plugins.goodreads_quotes",
    "plugins.series",
    "plugins.statistics",
    "plugins.search",
]
SUMMARY_USE_FIRST_PARAGRAPH = True
WITH_FUTURE_DATES = False
MATH_JAX = {
    "linebreak_automatic": True,
}

DIRECT_TEMPLATES = ("index", "tags", "categories", "archives", "search")
SEARCH_SAVE_AS = "search.html"
SEARCH_URL = "search.html"
STORK_INPUT_OPTIONS = {
    "html_selector": ".article-content",
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

GOODREADS_ACTIVITY_FEED = {
    "currently_reading": "https://www.goodreads.com/review/list_rss/109326321?key=3I5TuNfj-aUSty_wg0vzJhR3GxSlg6BKJdcqnhIF5wEZ8xuH&shelf=currently-reading",
    # "mathematics": "https://www.goodreads.com/review/list_rss/109326321?key=3I5TuNfj-aUSty_wg0vzJhR3GxSlg6BKJdcqnhIF5wEZ8xuH&shelf=mathematics",
}
GOODREADS_QUOTES = "https://www.goodreads.com/quotes/list_rss/109326321-joana"

RECENT_ARTICLES_COUNT = 5
RECENT_ARTICLE_SUMMARY = True
LANDING_PAGE_TITLE = "Welcome to JoJo's Blog"
PROJECTS = [
    {
        "name": "LLMs Journey",
        "url": "https://github.com/JoeJoe1313/LLMs-Journey",
        "description": "Collection of various experiments with Large Language Models",
    },
    {
        "name": "PaliGemma Image Segmentation",
        "url": "https://github.com/JoeJoe1313/PaliGemma-Image-Segmentation",
        "description": "An API service for performing image segmentation based on"
        " text prompts using Google's PaliGemma 2 mix model, built with FastAPI, JAX/Flax, and Transformers.",
    },
]
USE_SHORTCUT_ICONS = True
