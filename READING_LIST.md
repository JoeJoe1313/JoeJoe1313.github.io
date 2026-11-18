# Automatic Goodreads updates

The **Pelican Build & Deploy** workflow checks Goodreads once during each deployment, immediately before building the site. A push to `master` or a manual run of the workflow triggers the check. Changes you make on Goodreads appear with the next successful refresh and deployment.

The refresh reads the public “Currently Reading” and “Favourite” bookshelf widgets and Joana’s public quotes page. It validates all three sources before replacing the reading list in the build workspace. New books use the cover supplied by the widget when available.

GitHub Actions caches the reading list between builds. If Goodreads is unavailable or returns incomplete data, the build logs a warning and uses the cached list, or the copy in `content/data/reading-list.json` if the cache is unavailable. The **Refresh Goodreads shelves and quotes** step in the deployment log shows what happened.

For a local preview, run `.venv/bin/python scripts/sync_goodreads.py` to refresh the list, then `make html PELICAN=.venv/bin/pelican` to render `output/interests.html`.
