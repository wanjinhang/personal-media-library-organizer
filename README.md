# Personal Media Library Organizer

A small Python command-line tool for looking up movie, TV show, and anime metadata from [The Movie Database (TMDB)](https://www.themoviedb.org/), to help organize a private media library.

个人影视库元数据查询工具：核对片名、年份、季数和集数，为后续规范文件命名提供参考。

## Project status

This is an early, read-only prototype. The implemented commands search movie/TV metadata and retrieve a season's episode list. They do not rename, move, delete, upload, or download video files. Live API access requires your own TMDB credential; offline command-line and mocked API checks do not verify live service access.

Filename planning and reviewed batch renaming are planned features, not implemented capabilities. Long-running anime may require manual mapping between absolute episode numbers and TMDB season numbering.

## Requirements

- Python 3.10 or later.
- A TMDB account and API Read Access Token.
- Network access to `api.themoviedb.org`.

Only the Python standard library is used. No third-party packages are required.

## Quick start

```console
python tmdb_library.py --help
python tmdb_library.py search movie "The Wandering Earth" --year 2019
python tmdb_library.py search tv "Reply 1988" --year 2015
python tmdb_library.py episodes 1399 1
```

The last example uses a sample TMDB series ID. Use the ID returned by your own search when inspecting another show. Season `0` is for specials. Search currently returns the first page of results only.

The program securely prompts for the **API Read Access Token** when run interactively. Alternatively, it reads the existing `TMDB_READ_ACCESS_TOKEN` environment variable. It does not save credentials, create an `.env` file, or print credentials. JSON metadata is written to standard output; the default metadata language is `zh-CN`.

For English metadata:

```console
python tmdb_library.py --language en-US search movie "The Wandering Earth" --year 2019
```

## Intended naming workflow

1. Search TMDB to identify a movie or show.
2. Verify the title, release year, and relevant season/episode information.
3. Prepare a filename mapping and review ambiguous matches.
4. Apply renaming only after reviewing the mapping in a future version.

Illustrative filename formats:

```text
Movie Title.2019.1080p.mkv
TV Show.2015.S01E01.1080p.mkv
TV Show.2015.S00E01.mkv
```

Keep edition, language, and source details where useful. Do not alter internal Blu-ray disc structures. Sidecar subtitles need coordinated names when renaming is eventually implemented.

## API application

See [API application details](docs/API_APPLICATION.md) for the project purpose and a suggested application summary. This project is intended for private, non-commercial use. It does not distribute video files or resell TMDB data. This repository is not an official VidHub or TMDB project.

## About and attribution

Metadata is provided by [The Movie Database (TMDB)](https://www.themoviedb.org/).

> This product uses the TMDB API but is not endorsed or certified by TMDB.

The same notice appears in CLI help/version output and metadata output. TMDB data and images remain subject to TMDB's terms; this project does not claim ownership of them. The current CLI does not display images or posters. Any future graphical interface should use an approved TMDB logo and attribution according to the [official requirements](https://developer.themoviedb.org/docs/faq).

## Official references

- [TMDB API getting started](https://developer.themoviedb.org/docs/getting-started)
- [Application authentication](https://developer.themoviedb.org/docs/authentication-application)
- [Movie search](https://developer.themoviedb.org/reference/search-movie)
- [TV search](https://developer.themoviedb.org/reference/search-tv)
- [Season details](https://developer.themoviedb.org/reference/tv-season-details)
- [VidHub file naming convention](https://zh.vidhub.okaapps.com/vidhub-file-naming-convention/)
