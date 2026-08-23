#!/usr/bin/python3

# Copyright (c) 2012, Vassilios Karakoidas (vassilios.karakoidas@gmail.com)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""BibTeX parser used by biblio.py, also usable as a stand-alone library."""

import os
import re
from io import StringIO

from bibtex import bibtemplates


# Names from standard BibTeX style files (plain.bst, alpha.bst, ...)
MONTHS = {
    'jan': 'January',
    'feb': 'February',
    'mar': 'March',
    'apr': 'April',
    'may': 'May',
    'jun': 'June',
    'jul': 'July',
    'aug': 'August',
    'sep': 'September',
    'oct': 'October',
    'nov': 'November',
    'dec': 'December',
}

_SPECIAL = set('@{}(),"=#')


class ParseError(Exception):
    """A single entry could not be parsed; the scanner skips ahead."""


class BibtexEntry:
    def __init__(self, bibfile):
        self.key = ''
        self.data = {}
        self.btype = ''
        self.data['filename'] = bibfile

    def getKey(self, key):
        if key.lower().strip() == self.key.lower():
            return True
        return False

    def search(self, keywords):
        parts = [self.key, self.btype]
        for value in self.data.values():
            parts.append(str(value))
        haystack = ' '.join(parts).lower()
        return any(word.lower() in haystack for word in keywords)

    def keys(self):
        return self.data.keys()

    def authors(self):
        """Split the author field on BibTeX's 'and' separator."""
        raw = self.data.get('author', '').strip()
        if not raw:
            return []
        return [part.strip() for part in re.split(r'\s+and\s+', raw) if part.strip()]

    def __get_pdf_name(self):
        if not len(self.key):
            return None

        m = re.match(r'(.+/[^.]+)\.bib', self.data['filename'])
        if m is None:
            return None

        filename = '%s/%s.pdf' % (m.group(1).strip(), self.key.lower())
        if os.access(filename, os.R_OK):
            return filename

        return None

    def get_pdf(self):
        f = self.__get_pdf_name()
        if f is None:
            return 'No PDF file'
        return f

    def has_pdf(self):
        return self.__get_pdf_name() is not None

    def export(self):
        return self.__str__()

    def totext(self):
        return self.__str__()

    def tohtml(self):
        return self.__str__()

    @staticmethod
    def new_entry(entry_type):
        entry_dict = {
            'article': bibtemplates.new_article,
            'book': bibtemplates.new_book,
            'booklet': bibtemplates.new_booklet,
            'inbook': bibtemplates.new_inbook,
            'incollection': bibtemplates.new_incollection,
            'inproceedings': bibtemplates.new_inproceedings,
            'manual': bibtemplates.new_manual,
            'mastersthesis': bibtemplates.new_mastersthesis,
            'misc': bibtemplates.new_misc,
            'phdthesis': bibtemplates.new_phdthesis,
            'proceedings': bibtemplates.new_proceedings,
            'techreport': bibtemplates.new_techreport,
            'unpublished': bibtemplates.new_unpublished,
        }

        entry_func = entry_dict.get(entry_type, None)
        if entry_func is None:
            return 'Invalid type: %s' % (entry_type,)
        return entry_func()

    def __str__(self):
        result = StringIO()
        result.write('@%s{%s,\n' % (self.btype.lower().strip(), self.key.strip()))

        for k, v in self.data.items():
            result.write('\t%s = {%s},\n' % (k.title().strip(), str(v).strip()))

        filename = self.__get_pdf_name()
        if filename is not None:
            result.write('\tpdf-file = {%s},\n' % (filename,))

        result.write('}\n')
        return result.getvalue()


class _Scanner:
    def __init__(self, text):
        self.text = text
        self.n = len(text)
        self.i = 0

    def eof(self):
        return self.i >= self.n

    def peek(self):
        if self.eof():
            return ''
        return self.text[self.i]

    def get(self):
        if self.eof():
            raise ParseError('unexpected end of input')
        ch = self.text[self.i]
        self.i += 1
        return ch

    def skip_ws_and_comments(self):
        while not self.eof():
            ch = self.text[self.i]
            if ch.isspace():
                self.i += 1
            elif ch == '%':
                while not self.eof() and self.text[self.i] != '\n':
                    self.i += 1
            else:
                break

    def expect(self, wanted):
        self.skip_ws_and_comments()
        if self.peek() != wanted:
            raise ParseError("expected %r, got %r" % (wanted, self.peek()))
        return self.get()

    def read_name(self):
        self.skip_ws_and_comments()
        start = self.i
        while not self.eof():
            ch = self.text[self.i]
            if ch.isspace() or ch in _SPECIAL or ch == '%':
                break
            self.i += 1
        if start == self.i:
            raise ParseError('expected name')
        return self.text[start:self.i]

    def read_key(self, closer):
        self.skip_ws_and_comments()
        start = self.i
        while not self.eof():
            ch = self.text[self.i]
            if ch in (closer, ',', '{', '}', '(', ')') or ch.isspace() or ch == '%':
                break
            self.i += 1
        return self.text[start:self.i]

    def read_braced(self):
        if self.get() != '{':
            raise ParseError('expected {')
        depth = 1
        chunks = []
        while not self.eof() and depth:
            ch = self.get()
            if ch == '{':
                depth += 1
                chunks.append(ch)
            elif ch == '}':
                depth -= 1
                if depth:
                    chunks.append(ch)
            else:
                chunks.append(ch)
        if depth:
            raise ParseError('unbalanced braces')
        return ''.join(chunks)

    def read_quoted(self):
        if self.get() != '"':
            raise ParseError('expected "')
        chunks = []
        while not self.eof():
            ch = self.get()
            if ch == '"':
                return ''.join(chunks)
            if ch == '{':
                self.i -= 1
                chunks.append('{')
                chunks.append(self.read_braced())
                chunks.append('}')
            else:
                chunks.append(ch)
        raise ParseError('unterminated quoted string')

    def read_number(self):
        start = self.i
        while not self.eof() and self.text[self.i].isdigit():
            self.i += 1
        if start == self.i:
            raise ParseError('expected number')
        return self.text[start:self.i]

    def skip_balanced(self, opener, closer):
        depth = 1
        while not self.eof() and depth:
            ch = self.get()
            if ch == '"':
                self.i -= 1
                try:
                    self.read_quoted()
                except ParseError:
                    return
            elif ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1


def _collapse_ws(value):
    collapsed = re.sub(r'\s+', ' ', value)
    stripped = collapsed.strip()
    if stripped:
        return stripped
    return collapsed


class BibParser:
    """Scan a BibTeX database and return BibtexEntry records."""

    def __init__(self, text, source='<string>', strings=None):
        self.scanner = _Scanner(text)
        self.source = source
        self.strings = dict(MONTHS)
        if strings:
            self.strings.update({k.lower(): v for k, v in strings.items()})
        self.preambles = []
        self.entries = []

    def parse(self):
        sc = self.scanner
        while not sc.eof():
            sc.skip_ws_and_comments()
            if sc.eof():
                break
            if sc.peek() != '@':
                sc.i += 1
                continue
            try:
                self._parse_item()
            except ParseError:
                self._recover()
        self._resolve_crossrefs()
        return self.entries

    def _recover(self):
        sc = self.scanner
        while not sc.eof() and sc.peek() != '@':
            sc.i += 1

    def _parse_item(self):
        sc = self.scanner
        sc.expect('@')
        etype = sc.read_name()
        sc.skip_ws_and_comments()
        opener = sc.peek()
        if opener == '{':
            closer = '}'
        elif opener == '(':
            closer = ')'
        else:
            raise ParseError('expected { or ( after @%s' % etype)
        sc.get()

        kind = etype.lower()
        if kind == 'comment':
            sc.skip_balanced(opener, closer)
            return
        if kind == 'preamble':
            self._parse_preamble(closer)
            return
        if kind == 'string':
            self._parse_string(closer)
            return

        self._parse_record(etype, closer)

    def _parse_preamble(self, closer):
        sc = self.scanner
        sc.skip_ws_and_comments()
        value = self._parse_value()
        self.preambles.append(value)
        sc.skip_ws_and_comments()
        if sc.peek() == ',':
            sc.get()
        sc.skip_ws_and_comments()
        if sc.peek() == closer:
            sc.get()

    def _parse_string(self, closer):
        sc = self.scanner
        name, value = self._parse_assignment()
        self.strings[name.lower()] = value
        sc.skip_ws_and_comments()
        if sc.peek() == closer:
            sc.get()

    def _parse_record(self, etype, closer):
        sc = self.scanner
        key = sc.read_key(closer)
        sc.skip_ws_and_comments()
        if sc.peek() == ',':
            sc.get()

        entry = BibtexEntry(self.source)
        entry.btype = etype
        entry.key = key

        while True:
            sc.skip_ws_and_comments()
            if sc.eof():
                raise ParseError('unterminated entry %s' % key)
            if sc.peek() == closer:
                sc.get()
                break
            name, value = self._parse_assignment()
            entry.data[name.lower()] = value
            sc.skip_ws_and_comments()
            if sc.peek() == ',':
                sc.get()

        self.entries.append(entry)

    def _parse_assignment(self):
        sc = self.scanner
        name = sc.read_name()
        sc.expect('=')
        value = self._parse_value()
        return name, value

    def _parse_value(self):
        parts = [self._parse_simple_value()]
        sc = self.scanner
        while True:
            sc.skip_ws_and_comments()
            if sc.peek() != '#':
                break
            sc.get()
            parts.append(self._parse_simple_value())
        return ''.join(parts)

    def _parse_simple_value(self):
        sc = self.scanner
        sc.skip_ws_and_comments()
        ch = sc.peek()
        if ch == '{':
            return _collapse_ws(sc.read_braced())
        if ch == '"':
            return _collapse_ws(sc.read_quoted())
        if ch.isdigit():
            return sc.read_number()
        name = sc.read_name()
        return self.strings.get(name.lower(), name)

    def _resolve_crossrefs(self):
        by_key = {e.key.lower(): e for e in self.entries if e.key}
        for entry in self.entries:
            ref = entry.data.get('crossref')
            if not ref:
                continue
            parent = by_key.get(ref.lower())
            if parent is None:
                continue
            for field, value in parent.data.items():
                if field in ('filename', 'crossref'):
                    continue
                if field not in entry.data:
                    entry.data[field] = value


def parse_string(text, name='<string>', strings=None):
    """Parse a BibTeX database from a string. Returns a list of BibtexEntry."""
    return BibParser(text, source=name, strings=strings).parse()


def parse_bib(bibfile, strings=None):
    """Parse a .bib file. Returns a list of BibtexEntry (never contains None)."""
    with open(bibfile, 'r', encoding='utf-8', errors='replace') as handle:
        text = handle.read()
    return parse_string(text, name=bibfile, strings=strings)


def parse(source, strings=None):
    """Parse a filesystem path or a BibTeX string."""
    if os.path.isfile(source):
        return parse_bib(source, strings)
    return parse_string(source, strings=strings)
