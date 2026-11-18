import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit

from scripts.sync_goodreads import QUOTES, SNAPSHOT, USER, public_quotes, refresh, widget_books


def widget(shelf):
    key = shelf.replace("-", "_")
    markup = f"""
    <div class="gr_custom_container_{key}"><h2><a href="https://www.goodreads.com/review/list/{USER}?shelf={shelf}">Books</a></h2>
    <div class="gr_custom_each_container_{key}">
    <div class="gr_custom_title_{key}"><a href="/review/show/42">Reader's Guide</a></div>
    <div class="gr_custom_author_{key}"><a>Test Author</a></div>
    <div class="gr_custom_book_container_{key}"><a><img src="https://i.gr-assets.com/images/books/123l/123456789._SX98_.jpg"></a></div>
    </div></div>"""
    literal = json.dumps(markup)[1:-1].replace("'", r"\'")
    return f"var widget_code = '{literal}';"


def quote_page(page, total):
    return f"""
    <title>Quotes - Joana Showing {page}-{page} of {total}</title>
    <div class="userQuoteContainer">
    <div class="quoteText">“Quote {page}”<br> ― <span class="authorOrTitle">A. Writer,</span>
    <script>unrelated widget</script></div>
    <a href="/quotes/{page}-sample">likes</a></div>"""


class ReadingSyncTests(unittest.TestCase):
    def test_widget_reads_new_book_cover_and_escaped_title(self):
        books = widget_books({"name": "favourite"}, lambda url: widget("favourite"))
        self.assertEqual(books[0]["title"], "Reader's Guide")
        self.assertEqual(books[0]["id"], "123456789")
        self.assertTrue(books[0]["cover_url"].startswith("https://i.gr-assets.com/"))

    def test_rejects_cross_shelf_cache_and_sign_in_pages(self):
        for result in (widget("favourite"), "<title>Sign in</title>"):
            with self.subTest(result=result), self.assertRaises(ValueError):
                widget_books({"name": "currently-reading"}, lambda url: result)

    def test_quote_pagination_stops_on_duplicate(self):
        read = Mock(side_effect=[quote_page(1, 2), quote_page(2, 2)])
        result = public_quotes(read)
        self.assertEqual([q["text"] for q in result], ["“Quote 1”", "“Quote 2”"])
        self.assertEqual(read.call_args.args, (QUOTES + "?page=2",))
        with self.assertRaises(ValueError):
            public_quotes(lambda url: quote_page(1, 2))

    def test_partial_fetch_failure_preserves_snapshot_and_no_change_skips_write(self):
        def read(url):
            if url.startswith(QUOTES):
                return quote_page(1, 1)
            return widget(parse_qs(urlsplit(url).query)["shelf"][0])
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "snapshot.json"
            original = SNAPSHOT.read_bytes()
            path.write_bytes(original)
            with self.assertRaises(ValueError):
                refresh(path, lambda url: "<title>Sign in</title>" if url == QUOTES else read(url))
            self.assertEqual(path.read_bytes(), original)
            refresh(path, read)
            self.assertNotEqual(path.read_bytes(), original)
            identity = path.stat().st_ino, path.stat().st_mtime_ns
            refresh(path, read)
            self.assertEqual((path.stat().st_ino, path.stat().st_mtime_ns), identity)
