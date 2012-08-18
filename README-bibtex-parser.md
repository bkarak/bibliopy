bibtex-parser
=============

The bibtex parser used in *biblio.py* application, can be used stand-alone library to parse bibtex files.

Usage
-----
The library can be imported with an import statement. A bibtex file is loaded with the usage of <code>bibparse.parse</code> method. For example,

<pre>
from bibtex import bibparse

bibtex_entries = bibparse.parse('mycollection.bib')
</pre>

The results are instances of the <code>BibtexEntry</code> class.

Projects
--------
The bibtex-parser is used in the following projects:

* [citeproc-py](https://github.com/brechtm/citeproc-py) - citeproc-py is a CSL processor written in Python. It aims to implement CSL 1.0, but already supports some CSL 1.0.1 features.
* [bib2coins](https://github.com/robintw/bib2coins) - bib2coins is a simple tool which will convert BibTeX files to COINS metadata (see [http://ocoins.info/](http://ocoins.info/)) ready for inclusion in a webpage.