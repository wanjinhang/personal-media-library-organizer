"""Read-only TMDB metadata helper for a personal media library."""

import argparse
import getpass
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = "https://api.themoviedb.org/3"
ATTRIBUTION = (
    "This product uses the TMDB API but is not endorsed or certified by TMDB."
)


def nonnegative(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("Must be zero or greater.")
    return number


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Must be greater than zero.")
    return number


def request_metadata(endpoint, params, token):
    url = f"{API_BASE}/{endpoint}?{urlencode(params)}"
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "PersonalMediaLibraryOrganizer/0.1",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        messages = {
            401: "Authentication failed. Check your TMDB API Read Access Token.",
            404: "TMDB could not find the requested resource.",
            429: "TMDB rate limit reached. Wait before trying again.",
        }
        raise RuntimeError(messages.get(error.code, f"TMDB HTTP error {error.code}.")) from None
    except (URLError, TimeoutError, OSError):
        raise RuntimeError("Could not connect to TMDB. Check your network and try again.") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("TMDB returned an invalid JSON response.") from None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Search TMDB and inspect season episode metadata. Does not change media files.",
        epilog=ATTRIBUTION,
    )
    parser.add_argument("--version", action="version", version=f"0.1.0\n{ATTRIBUTION}")
    parser.add_argument("--language", default="zh-CN", help="Metadata language (default: zh-CN).")
    commands = parser.add_subparsers(dest="command", required=True)
    search = commands.add_parser("search", help="Search the first page of movie or TV matches.")
    search.add_argument("kind", choices=["movie", "tv"])
    search.add_argument("query")
    search.add_argument("--year", type=positive, help="Movie release year or TV first-air year.")
    episodes = commands.add_parser("episodes", help="List the episodes in a TMDB season.")
    episodes.add_argument("series_id", type=positive)
    episodes.add_argument("season", type=nonnegative, help="Use 0 for specials.")
    args = parser.parse_args(argv)
    token = os.environ.get("TMDB_READ_ACCESS_TOKEN", "").strip()
    if not token:
        if not sys.stdin.isatty():
            parser.error("Set TMDB_READ_ACCESS_TOKEN or run interactively to enter it securely.")
        token = getpass.getpass("TMDB API Read Access Token: ").strip()
    if not token:
        parser.error("A TMDB API Read Access Token is required.")
    params = {"language": args.language}
    if args.command == "search":
        endpoint = f"search/{args.kind}"
        params.update(query=args.query, include_adult="false", page=1)
        if args.year:
            params["primary_release_year" if args.kind == "movie" else "first_air_date_year"] = args.year
    else:
        endpoint = f"tv/{args.series_id}/season/{args.season}"
    try:
        data = request_metadata(endpoint, params, token)
        records = data.get("results", []) if args.command == "search" else data.get("episodes", [])
        print(json.dumps({"source": "TMDB", "attribution": ATTRIBUTION, "records": records}, ensure_ascii=False, indent=2))
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
