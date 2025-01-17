import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from pelican import signals


class TheoremCounter:
    def __init__(self):
        self.counters = {
            "theorem": 0,
            "definition": 0,
            "lemma": 0,
            "proof": 0,
            "corollary": 0,
        }

    def increment(self, env_type):
        self.counters[env_type] = self.counters.get(env_type, 0) + 1
        return self.counters[env_type]


class TheoremPreprocessor(Preprocessor):
    def __init__(self, md):
        super().__init__(md)
        self.counter = TheoremCounter()

    def run(self, lines):
        new_lines = []
        is_in_env = False
        current_env = None
        env_content = []

        # Define environment styles
        env_styles = {
            "theorem": ("Theorem", "theorem-style"),
            "definition": ("Definition", "definition-style"),
            "lemma": ("Lemma", "theorem-style"),
            "proof": ("Proof", "proof-style"),
            "corollary": ("Corollary", "theorem-style"),
        }

        for line in lines:
            # Check for environment start
            env_start = re.match(
                r"\\begin{(theorem|definition|lemma|proof|corollary)}", line
            )
            if env_start:
                is_in_env = True
                current_env = env_start.group(1)
                env_number = (
                    self.counter.increment(current_env)
                    if current_env != "proof"
                    else ""
                )
                env_title, env_class = env_styles[current_env]

                # Create environment header
                if current_env == "proof":
                    new_lines.append(f'<div class="{env_class}">')
                    new_lines.append(
                        f'<span class="env-name"><strong>{env_title}.</strong></span>'
                    )
                else:
                    new_lines.append(f'<div class="{env_class}">')
                    new_lines.append(
                        f'<span class="env-name"><strong>{env_title} {env_number}.</strong></span>'
                    )
                continue

            # Check for environment end
            elif r"\end{" in line:
                is_in_env = False
                if current_env == "proof":
                    new_lines.append('<span class="qed">□</span>')
                new_lines.append("</div>")
                continue

            if is_in_env:
                new_lines.append(line)
            else:
                new_lines.append(line)

        return new_lines


class TheoremExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(TheoremPreprocessor(md), "theorem_environments", 175)


def add_theorem_styles(generator):
    """Add CSS styles for theorem environments"""
    if not hasattr(generator, "settings"):
        return

    css = """
    <style>
        .theorem, .definition, .lemma, .corollary {
            margin: 1em 0;
            padding: 0.5em 1em;
            border-left: 3px solid #4a5568;
            background-color: #f8f9fa;
        }
        
        .env-name {
            display: block;
            margin-bottom: 0.5em;
            color: #1a202c;
        }
        
        .env-name strong {
            font-weight: 800;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        
        .theorem p, .lemma p, .corollary p {
            font-style: italic;
            margin: 0;
        }
        
        .proof {
            margin: 1em 0;
            padding: 0.5em 1em;
        }
        
        .proof .env-name {
            font-style: italic;
        }
        
        .qed {
            float: right;
            margin-top: 0.5em;
        }
    </style>
    """

    if not hasattr(generator, "custom_css"):
        generator.custom_css = ""
    generator.custom_css += css


def init_plugin(pelican):
    config = pelican.settings.get("MARKDOWN", {})
    if "extensions" not in config:
        config["extensions"] = []
    config["extensions"].append(TheoremExtension())
    pelican.settings["MARKDOWN"] = config


def register():
    signals.initialized.connect(init_plugin)
    signals.generator_init.connect(add_theorem_styles)
