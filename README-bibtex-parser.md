bibtex-parser
=============

The bibtex parser used in *biblio.py* can also be used as a stand-alone library to parse bibtex files.

Usage
-----
Import the library and load a file with `bibparse.parse_bib`. For example,

    from bibtex import bibparse

    bibtex_entries = bibparse.parse_bib('mycollection.bib')

The results are instances of the `BibtexEntry` class.

Each entry exposes:

* `key` — the BiBTeX citation key
* `btype` — the entry type (`article`, `book`, …)
* `data` — a dictionary of fields
* `search(keywords)` — true if any field contains one of the keywords
* `export()` / `__str__()` — the entry rendered as BiBTeX
* `get_pdf()` — path of the associated PDF, if one exists
* `BibtexEntry.new_entry(entry_type)` — a template for a new entry

Projects
--------
The bibtex-parser is used in the following projects:

* [citeproc-py](https://github.com/brechtm/citeproc-py) - citeproc-py is a CSL processor written in Python. It aims to implement CSL 1.0, but already supports some CSL 1.0.1 features.
* [bib2coins](https://github.com/robintw/bib2coins) - bib2coins is a simple tool which will convert BibTeX files to COINS metadata (see [http://ocoins.info/](http://ocoins.info/)) ready for inclusion in a webpage.
