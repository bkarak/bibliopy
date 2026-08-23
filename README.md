biblio.py - easy to use bibtex utility in Python
================================================

What is this biblio.py?
-----------------------

**biblio.py** is a simple utility, written in Python. Its purpose is to provide an easy way to search and store all BiBTeX repositories.

Personally, i used most of the programs that do that work, but i wanted a command line (portable also) solution. In addition, i wanted it to be VERY resilient to errors.

So i wrote this (for the Greek Linux Format, download article code here) as a simple python-based solution, designed with the following requirements in mind:

* Command-line
* Portable
* Resilient to errors

Requires **Python 3**. See also [bibtex-parser](README-bibtex-parser.md).

Initialisation
--------------
On the first run, `biblio.py` creates `~/.biblio-py/` and an empty `~/.biblio-py/repositories` file. After that, add directories that contain your `.bib` files:

    $ python3 biblio.py addpath /path/to/bibtex
    $ python3 biblio.py list
    $ python3 biblio.py count

Each line in `~/.biblio-py/repositories` is a directory that will be scanned recursively for `*.bib` files.

Remember, the tool is written to be resilient to errors. So, if you happen to have duplicate entries (or entries with missing tags), no worries, *biblio.py* will not complain. Just add your BiBTeX dirs, search and export.

Usage
-----

    $ python3 biblio.py

    bibliography utility v0.59

    usage: biblio.py <directive> <arguments>

    new <type>         - Print a new entry, one of the following:
                         (article, book, booklet, inbook, incollection,
                          inproceedings, manual, mastersthesis, misc,
                          phdthesis, proceedings, techreport, unpublished)
    key                - Export a specific key
    addpath            - Add a repository path
    list               - List repository paths (also checks their validity)
    search <keyword>   - search ALL bibtex tags for specific entries
    count              - Count all bibtex entries and print statistics
    export <keys...>   - Extracts the selected keys
    expfile <file>     - Read the selected keys from a specified file and export the entries
    texmode <files...> - Search a latex file and export its entries
    pdf <keys...>      - Prints the path of the associated PDF file
    help               - Prints the online help

An interesting feature is the *expfile* argument that exports all the BiBTeX keys that are written to a text file. The keys should occupy one line each (subject to change).

PDF files
---------
If a PDF sits next to the `.bib` file, *biblio.py* will attach it to the matching entry. For `/home/bkarak/foo.bib`, PDFs belong in `/home/bkarak/foo/` and must be named after the entry key (lowercase), for example `grsh00.pdf`. Export then adds a `pdf-file` field, and `pdf <key>` prints that path.

LaTeX
-----
One usage i usually like is mixture with latex. I use a simplistic makefile to simplify the building process, and looks something like that:

    pdf:
	    python3 biblio.py expfile bib.keys > document.bib
	    pdflatex document.tex
	    bibtex document
	    pdflatex document.tex
	    pdflatex document.tex

Since version 0.5 biblio.py has the *texmode* directive. With this you can instruct biblio.py to scan a TeX file for citations (`\cite{KEY}`) and export the selected entries (if they are in the repository). So the previous example can be modified like this:

    pdf:
	    python3 biblio.py texmode document.tex > document.bib
	    pdflatex document.tex
	    bibtex document
	    pdflatex document.tex
	    pdflatex document.tex

Latest version is **v0.59**.
