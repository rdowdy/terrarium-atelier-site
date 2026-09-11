# The Atelier — public gallery

Static site generated from the sealed Atelier directory. The Atelier itself is
never written to; `build.py` reads it and emits `docs/`, copying each hung work
verbatim. GitHub Pages serves `docs/` from the `main` branch.

Rebuild and deploy by hand:

    python build.py
    git add -A && git commit -m "Epoch NNNN" && git push

`deploy.ps1` does the same unattended and is what the nightly scheduled task runs.
