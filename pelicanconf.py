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
ARCHIVES_SAVE_AS = ""
THEME = "themes/notmyidea"
STATIC_PATHS = [
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
    ("LinkedIn", "https://www.linkedin.com/in/joana-levtcheva-479844164/"),
    # ("Another social link", "#"),
)

DEFAULT_PAGINATION = 5

PLUGINS = [
    "plugins.summary",
    "plugins.render_math",
    "plugins.liquid_tags.include_code",
    "plugins.liquid_tags.include_code_collapsible",
    "plugins.goodreads_activity",
    "plugins.goodreads_quotes",
]
SUMMARY_USE_FIRST_PARAGRAPH = True
WITH_FUTURE_DATES = False
MATH_JAX = {
    "linebreak_automatic": True,
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

GOODREADS_ACTIVITY_FEED = {
    "currently_reading": "https://www.goodreads.com/review/list_rss/109326321?key=3I5TuNfj-aUSty_wg0vzJhR3GxSlg6BKJdcqnhIF5wEZ8xuH&shelf=currently-reading",
    # "mathematics": "https://www.goodreads.com/review/list_rss/109326321?key=3I5TuNfj-aUSty_wg0vzJhR3GxSlg6BKJdcqnhIF5wEZ8xuH&shelf=mathematics",
}
GOODREADS_QUOTES = "https://www.goodreads.com/quotes/list_rss/109326321-joana"
