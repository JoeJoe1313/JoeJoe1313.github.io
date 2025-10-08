"""jinja2content: Pelican plugin that processes Markdown files as Jinja templates."""

import os
from tempfile import NamedTemporaryFile

from jinja2 import ChoiceLoader, Environment, FileSystemLoader
from pelican import signals
from pelican.readers import HTMLReader, MarkdownReader, RstReader
from pelican.utils import pelican_open


class JinjaContentMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # will look first in 'JINJA2CONTENT_TEMPLATES', by default the
        # content root path, then in the theme's templates
        local_dirs = self.settings.get("JINJA2CONTENT_TEMPLATES", ["."])
        local_dirs = [
            os.path.join(self.settings["PATH"], folder) for folder in local_dirs
        ]
        theme_dir = os.path.join(self.settings["THEME"], "templates")

        loaders = [FileSystemLoader(_dir) for _dir in local_dirs + [theme_dir]]
        if "JINJA_ENVIRONMENT" in self.settings:  # pelican 3.7
            jinja_environment = self.settings["JINJA_ENVIRONMENT"]
        else:
            jinja_environment = {
                "trim_blocks": True,
                "lstrip_blocks": True,
                "extensions": self.settings["JINJA_EXTENSIONS"],
            }
        self.env = Environment(loader=ChoiceLoader(loaders), **jinja_environment)
        if "JINJA_FILTERS" in self.settings:
            self.env.filters.update(self.settings["JINJA_FILTERS"])
        if "JINJA_GLOBALS" in self.settings:
            self.env.globals.update(self.settings["JINJA_GLOBALS"])
        if "JINJA_TEST" in self.settings:
            self.env.tests.update(self.settings["JINJA_TESTS"])

    def read(self, source_path):
        with pelican_open(source_path) as original_text:
            if not self._should_render_with_jinja(original_text):
                return super().read(source_path)

            rendered_text = self.env.from_string(original_text).render()

        with NamedTemporaryFile(delete=False) as f:
            f.write(rendered_text.encode())
            f.close()
            content, metadata = super().read(f.name)
            os.unlink(f.name)
            return content, metadata

    def _should_render_with_jinja(self, text):
        """Return True when front matter sets ``jinja`` to a truthy value."""
        if not text.startswith("---"):
            return False

        delimiter = "---"
        lines = text.splitlines()
        try:
            start = lines.index(delimiter)
            end = lines.index(delimiter, start + 1)
        except ValueError:
            return False

        for raw_line in lines[start + 1 : end]:
            if ":" not in raw_line:
                continue
            key, value = raw_line.split(":", 1)
            if key.strip().lower() != "jinja":
                continue
            normalized = value.strip().lower()
            return normalized in {"true", "yes", "on", "1"}
        return False


class JinjaMarkdownReader(JinjaContentMixin, MarkdownReader):
    pass


class JinjaRstReader(JinjaContentMixin, RstReader):
    pass


class JinjaHTMLReader(JinjaContentMixin, HTMLReader):
    pass


def add_reader(readers):
    """Add Jinja readers."""
    for Reader in [JinjaMarkdownReader, JinjaRstReader, JinjaHTMLReader]:
        for ext in Reader.file_extensions:
            readers.reader_classes[ext] = Reader


def register():
    """Register the plugin."""
    signals.readers_init.connect(add_reader)
