"""Refresh the Interests page from Goodreads' public widgets and quote list."""

import json
import re
import sys
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlsplit
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from plugins.reading_list import load_reading_list, validate_reading_list

BASE = "https://www.goodreads.com"
USER = "109326321"
QUOTES = f"{BASE}/quotes/list/{USER}-joana"
SNAPSHOT = ROOT / "content/data/reading-list.json"


def fetch(url):
    request = Request(url, headers={"User-Agent": "JoJosBlog/1.0 (+https://joejoe1313.github.io)"})
    with urlopen(request, timeout=25) as response:
        body = response.read(5_000_001)
    if len(body) > 5_000_000:
        raise ValueError("Unexpectedly large Goodreads response")
    return body.decode("utf-8")


def widget_books(shelf, read=fetch):
    name = shelf["name"]
    widget_id = name.replace("-", "_")
    # Give each shelf its own widget path as well as a shelf parameter.
    label = quote(f"Joana's {name} books", safe="")
    query = urlencode(dict(shelf=name, num_books=100, widget_id=widget_id,
                           cover_size="medium", title="yes", author="yes",
                           show_cover="true", shelf_link="yes", sort="date_added", order="d"))
    script = read(f"{BASE}/review/custom_widget/{USER}.{label}?{query}")
    # Extract the widget's string literal as data. Never execute the JavaScript.
    match = re.search(r"(?m)^\s*var widget_code\s*=\s*'((?:\\.|[^'\\\n])*)';?\s*$", script)
    if not match:
        raise ValueError(f"{name}: unrecognized widget response")
    fragment = json.loads('"' + match[1].replace(r"\'", "'") + '"')
    dom = BeautifulSoup(fragment, "html.parser")
    container = dom.select_one(f".gr_custom_container_{widget_id}")
    header = container.select_one("h2 a[href]") if container else None
    link = urlsplit(header["href"]) if header else None
    if (not link or not re.fullmatch(rf"/review/list/{USER}(?:-[^/]+)?", link.path)
            or parse_qs(link.query).get("shelf") != [name]):
        raise ValueError(f"{name}: Goodreads returned the wrong shelf")
    entries = container.select(f".gr_custom_each_container_{widget_id}")
    if not entries and (not container.select_one('img[alt="goodreads.com"]')
                        or container.select_one('a[href*="/review/show/"], a[href*="/book/show/"]')):
        raise ValueError(f"{name}: incomplete bookshelf markup")
    if len(entries) >= 100:
        raise ValueError(f"{name}: reached widget limit, cannot confirm a complete shelf")

    books = []
    for entry in entries:
        title = entry.select_one(f".gr_custom_title_{widget_id} a[href]")
        author = entry.select_one(f".gr_custom_author_{widget_id} a")
        if not title or not author:
            raise ValueError(f"{name}: incomplete book entry")
        cover = entry.select_one(f".gr_custom_book_container_{widget_id} img")
        cover_url = cover.get("src", "") if cover else ""
        review = re.fullmatch(r"/review/show/(\d+)", urlsplit(title["href"]).path)
        if not review:
            raise ValueError(f"{name}: unrecognized book link")
        book_id = re.search(r"/(\d+)(?:\.[^/]*)?\.(?:jpg|png)$", urlsplit(cover_url).path)
        # Some editions have placeholder covers. Their review permalink still works.
        identifier = book_id[1] if book_id else review[1]
        url = f"{BASE}/book/show/{identifier}" if book_id else f"{BASE}/review/show/{identifier}"
        local = f"images/books/{identifier}.jpg"
        book = dict(id=identifier, url=url, title=title.get_text(" ", strip=True),
                    author=" ".join(author.stripped_strings), cover="")
        book["author"] = " ".join(book["author"].split())
        if cover and cover.parent.get("title"):
            book["title"] = cover.parent["title"]
        if book_id and (ROOT / "content" / local).is_file():
            book["cover"] = local
        elif cover_url:
            # Accept only Goodreads' known image hosts in the saved snapshot.
            remote = urlsplit(cover_url)
            if remote.scheme == "https" and remote.netloc in {"i.gr-assets.com", "images-na.ssl-images-amazon.com"}:
                book["cover_url"] = cover_url
        books.append(book)
    return books


def public_quotes(read=fetch):
    quotes = []
    seen = set()
    url = QUOTES
    for page in range(1, 101):
        dom = BeautifulSoup(read(url), "html.parser")
        title = dom.title.get_text(" ", strip=True) if dom.title else ""
        result = re.search(r"Showing\s+(\d+)\s*[-–]\s*(\d+)\s+of\s+(\d+)", title)
        if not title.startswith("Quotes - Joana") or not result:
            raise ValueError("Cannot confirm Goodreads quote list or count")
        for entry in dom.select(".userQuoteContainer"):
            body = entry.select_one(".quoteText")
            author = body.select_one("span.authorOrTitle") if body else None
            link = entry.select_one('a[href^="/quotes/"]')
            if not author or not link or not re.match(r"^/quotes/\d+", link["href"]):
                raise ValueError("Incomplete Goodreads quote")
            parts = []
            for node in body.descendants:
                if node is author:
                    break
                if isinstance(node, NavigableString):
                    parts.append(str(node))
            text = " ".join(" ".join(parts).split()).rstrip("―").rstrip()
            source = body.select_one('span[id^="quote_book_link"] a')
            permalink = urljoin(BASE, link["href"])
            if permalink in seen:
                raise ValueError("Duplicate quote during pagination")
            seen.add(permalink)
            quotes.append(dict(text=text, author=author.get_text(" ", strip=True).rstrip(","),
                               book=source.get_text(" ", strip=True) if source else "", url=permalink))
        if len(quotes) != int(result[2]):
            raise ValueError("Incomplete Goodreads quotes page")
        if len(quotes) == int(result[3]):
            return quotes
        url = f"{QUOTES}?page={page + 1}"
    raise ValueError("Goodreads quote pagination exceeded limit")


def refresh(path=SNAPSHOT, read=fetch):
    previous = load_reading_list(path)
    shelves = [{**shelf, "books": widget_books(shelf, read)} for shelf in previous["shelves"]]
    data = {**previous, "shelves": shelves, "quotes": public_quotes(read)}
    validate_reading_list(data)
    for shelf in shelves:
        print(f"{shelf['title']}: {len(shelf['books'])} books")
    print(f"Quotes: {len(data['quotes'])}")
    if previous == data:
        print("Reading list is current.")
        return
    data["updated"] = date.today().isoformat()
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
    Path(tmp.name).replace(path)
    print("Updated reading list.")


if __name__ == "__main__":
    refresh()
