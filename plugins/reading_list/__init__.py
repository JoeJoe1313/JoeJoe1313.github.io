"""Make a validated, local reading list available to Jinja content."""

import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

from pelican import signals


def validate_reading_list(data):
    """Reject broken data instead of silently publishing an empty Interests page."""
    if not isinstance(data, dict):
        raise ValueError("Reading list must be a JSON object")
    date.fromisoformat(data["updated"])
    if not isinstance(data.get("shelves"), list) or not isinstance(data.get("quotes"), list):
        raise ValueError("Reading list requires shelves and quotes arrays")

    def text(item, key):
        if not isinstance(item.get(key), str) or not item[key].strip():
            raise ValueError(f"Reading list entry requires a nonempty {key}")

    def link(item):
        text(item, "url")
        parsed = urlsplit(item["url"])
        if parsed.scheme != "https" or parsed.hostname != "www.goodreads.com":
            raise ValueError("Reading list links must use https://www.goodreads.com")

    names = set()
    book_count = 0
    for shelf in data["shelves"]:
        text(shelf, "name")
        text(shelf, "title")
        link(shelf)
        if not re.fullmatch(r"[a-z0-9-]+", shelf["name"]) or shelf["name"] in names:
            raise ValueError("Reading list shelf names must be unique URL slugs")
        names.add(shelf["name"])
        if not isinstance(shelf.get("books"), list):
            raise ValueError("Reading list shelves require a books array")
        ids = set()
        for book in shelf["books"]:
            for key in ("id", "title", "author"):
                text(book, key)
            link(book)
            if not book["id"].isdigit() or book["id"] in ids:
                raise ValueError("Reading list book IDs must be numeric and unique within a shelf")
            ids.add(book["id"])
            cover = book.get("cover", "")
            if not isinstance(cover, str) or (
                cover and not re.fullmatch(r"images/books/[a-zA-Z0-9_.-]+\.(jpg|jpeg|png|webp)", cover)
            ):
                raise ValueError("Book covers must be local files under images/books/")
            if book.get("cover_url"):
                remote = urlsplit(book["cover_url"])
                if remote.scheme != "https" or remote.netloc not in {
                    "i.gr-assets.com", "images-na.ssl-images-amazon.com"
                }:
                    raise ValueError("Invalid Goodreads cover URL")
        book_count += len(shelf["books"])
    for quote in data["quotes"]:
        text(quote, "text")
        text(quote, "author")
        link(quote)
    if not book_count and not data["quotes"]:
        raise ValueError("Reading list has no books or quotes; refusing to publish an empty page")
    return data


def load_reading_list(filename):
    try:
        return validate_reading_list(json.loads(Path(filename).read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        raise ValueError(f"Cannot load reading list from {filename}: {error}") from error


def add_to_jinja_globals(pelican_obj):
    data = load_reading_list(pelican_obj.settings["READING_LIST_DATA"])
    content_root = Path(pelican_obj.settings["PATH"])
    for shelf in data["shelves"]:
        for book in shelf["books"]:
            if book.get("cover") and not (content_root / book["cover"]).is_file():
                raise ValueError(f"Missing reading list cover: {book['cover']}")
    pelican_obj.settings.setdefault("JINJA_GLOBALS", {})["reading_list"] = data


def register():
    signals.initialized.connect(add_to_jinja_globals)
