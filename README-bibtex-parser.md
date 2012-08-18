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