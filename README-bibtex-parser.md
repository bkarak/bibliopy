bibtex-parser
=============

The bibtex parser used in *biblio.py* can also be used as a stand-alone library to parse bibtex files. Current version is **v0.60** (`bibtex.__version__`).

Usage
-----
Import the library and load a file with `bibparse.parse_bib`, or a string with `bibparse.parse_string`. `bibparse.parse` accepts either.

    from bibtex import bibparse

    bibtex_entries = bibparse.parse_bib('mycollection.bib')
    same = bibparse.parse('@article{x, title={Hello}, year=2020}')

The results are instances of the `BibtexEntry` class.

Each entry exposes:

* `key` — the BiBTeX citation key
* `btype` — the entry type (`article`, `book`, …)
* `data` — a dictionary of fields (plus `filename`, the source path or label)
* `search(keywords)` — true if the key, type, or any field contains one of the keywords
* `authors()` — the `author` field split on BibTeX `and`
* `export()` / `__str__()` — the entry rendered as BiBTeX
* `get_pdf()` — path of the associated PDF, if one exists
* `BibtexEntry.new_entry(entry_type)` — a template for a new entry

What is parsed
--------------
The scanner understands a full `.bib` database, not only one-field-per-line records:

* `@article`, `@book`, and any other entry type, including unknown types
* `@string` macros, expanded when a field uses the name as a bare identifier
* built-in month names (`jan` … `dec`)
* `@preamble` and `@comment` (recorded / skipped, not turned into entries)
* `%` comments outside values
* `{...}` and `(...)` entry delimiters
* nested braces (`title = {The {GNU} Project}`)
* quoted values (`title = "Hello"`)
* `#` concatenation (`title = {Hello} # { } # {World}`)
* bare numbers (`year = 2020`)
* multiline fields
* trailing commas
* UTF-8
* `crossref` — missing fields are copied from the referenced entry
* broken entries are skipped; later records in the same file are still parsed

Optional extra macros can be supplied:

    bibparse.parse_string(text, strings={'ieee': 'IEEE'})

`bibtex.bibvalidator.BibFields.validate_entry(entry)` checks required fields for the standard entry types (`author` or `editor` is accepted for `@book` / `@inbook`).

    $ python3 -m unittest tests.test_bibparse

Projects
--------
The bibtex-parser is used in the following projects:

* [citeproc-py](https://github.com/brechtm/citeproc-py) - citeproc-py is a CSL processor written in Python. It aims to implement CSL 1.0, but already supports some CSL 1.0.1 features.
* [bib2coins](https://github.com/robintw/bib2coins) - bib2coins is a simple tool which will convert BibTeX files to COINS metadata (see [http://ocoins.info/](http://ocoins.info/)) ready for inclusion in a webpage.
