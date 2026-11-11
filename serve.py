#!/usr/bin/env python3
"""
Static server for the guitar apps with clean (extensionless) app URLs.

Routes:
    /          -> index.html   (Fret Player)
    /tuner     -> tuner.html   (Guitar Tuner)
    /trainer   -> trainer.html (Chord Trainer)
    anything else falls back to normal static file serving from this directory.

Binds to loopback by default.

Usage: python3 serve.py [--port 8799] [--bind 127.0.0.1]
"""

import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# clean URL -> file on disk
ALIASES = {
    "/tuner": "/tuner.html",
    "/tuner/": "/tuner.html",
    "/trainer": "/trainer.html",
    "/trainer/": "/trainer.html",
    "/player": "/index.html",
    "/player/": "/index.html",
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def translate_path(self, path):
        # strip query/fragment for alias match
        clean = path.split("?", 1)[0].split("#", 1)[0]
        if clean in ALIASES:
            path = ALIASES[clean]
        return super().translate_path(path)

    def log_message(self, fmt, *args):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8799)
    ap.add_argument("--bind", default="127.0.0.1")
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.bind, args.port), Handler)
    print(f"guitar site: {args.bind}:{args.port} -> {DIRECTORY}")
    srv.serve_forever()


if __name__ == "__main__":
    main()
