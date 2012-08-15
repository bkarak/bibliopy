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

Usage
-----
`$ python biblio-py

bibliography utility v0.52

usage: biblio.py <directive> >arguments<

key               - Export a specific key
addpath           - Add a repository path
list              - Lists all repository paths (and checks their validity)
search <keyword>  - search ALL bibtex tags for specific entries
count             - Count all bibtex entries and print statistics
export <keys...>  - Extracts the selected keys
expfile <file>    - Read the selected keys from a specified file and export the entries
texmode <files...> - Search a latex file and exports its entries
help              - Prints the online help`
