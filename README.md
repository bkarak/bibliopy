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

See also [bibtex-parser](https://github.com/bkarak/bibliopy/blob/master/README-bibtex-parser.md)

Usage
-----
To initialise the program you just have to add some paths (directories that contain your bib files), and then perform search export or count. 

An interesting feature is the *expfile* argument that exports all the BiBTeX keys that are written to a text file. The keys should occupy one line each (subject to change). Be aware that unicode is not supported in this function. 

Remember, the tool is written to be resilient to errors. So, if you happen to have duplicate entries (or entries with missing tags), no worries, *biblio.py* will not complain. Just add your BiBTeX dirs, search and export.

    $ python biblio-py

    bibliography utility v0.56

    usage: biblio.py <directive> >arguments<

    key                - Export a specific key
    addpath            - Add a repository path
    list               - Lists all repository paths (and checks their validity)
    search <keyword>   - search ALL bibtex tags for specific entries
    count              - Count all bibtex entries and print statistics
    export <keys...>   - Extracts the selected keys
    expfile <file>     - Read the selected keys from a specified file and export the entries
    texmode <files...> - Search a latex file and exports its entries
    help               - Prints the online help

One usage i usually like is mixture with latex. I use a simplistic makefile to simplify the building process, and looks something like that:

    pdf:
	    biblio.py expfile bib.keys > document.bib
	    pdflatex document.tex
	    bibtex document
	    pdflatex document.tex
	    pdflatex document.tex

Since version 0.5 biblio.py has the texmode. With this directive you can instruct biblio.py to scan a TeX file for citations (\cite{KEY}) and export the selected entries (if there are in the repository ofc). So the previous example can be modified like this:

    pdf:
	    biblio.py textfile document.tex > document.bib
    	pdflatex document.tex
	    bibtex document
	    pdflatex document.tex
	    pdflatex document.tex

Latest version is **v0.56**.
