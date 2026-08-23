import os
import tempfile
import unittest

from bibtex import bibparse
from bibtex.bibvalidator import BibFields


COMPLEX_BIB = r"""
% file-level comment
@string{ieee = {IEEE}}
@string{space = { }}
@preamble{ "\newcommand{\noop}[1]{}" }

@article{multiline,
  author = {Jane Doe and John Smith},
  title = {A title that
           spans several
           lines},
  journal = {J. Testing},
  year = 2020,
  month = jan,
  note = {See url with percent: "http://ex.org/a%20b"}
}

@book{braces,
  title = {The {GNU} Project},
  author = {Stallman, Richard},
  year = {1984},
  publisher = ieee
}

@inproceedings{concat,
  title = {Hello} # space # {World},
  author = {Ada Lovelace},
  booktitle = "Conference on {Things}",
  year = 1843
}

@article(paren-key,
  title = {Parentheses work},
  author = {Someone},
  journal = {X},
  year = 2001,
)

@inproceedings{child,
  title = {A paper},
  author = {Kid, A},
  crossref = {parent}
}

@proceedings{parent,
  booktitle = {ICSE},
  year = 2011,
  editor = {Big Editor}
}

@comment{this is ignored entirely}

@article{broken
  title = {missing equals and closer}

@misc{recovered,
  title = {Still parsed after a broken neighbour},
  year = 1999
}
"""


class ParseStringTests(unittest.TestCase):
    def setUp(self):
        self.entries = bibparse.parse_string(COMPLEX_BIB, name='complex.bib')
        self.by_key = {e.key: e for e in self.entries}

    def test_skips_none_and_specials(self):
        self.assertNotIn(None, self.entries)
        keys = [e.key for e in self.entries]
        self.assertNotIn('', keys)
        self.assertNotIn('this is ignored entirely', keys)

    def test_multiline_and_bare_year_and_month(self):
        entry = self.by_key['multiline']
        self.assertEqual(entry.btype.lower(), 'article')
        self.assertEqual(entry.data['title'], 'A title that spans several lines')
        self.assertEqual(entry.data['year'], '2020')
        self.assertEqual(entry.data['month'], 'January')
        self.assertIn('%20', entry.data['note'])
        self.assertEqual(entry.data['filename'], 'complex.bib')

    def test_nested_braces_and_string_expansion(self):
        entry = self.by_key['braces']
        self.assertEqual(entry.data['title'], 'The {GNU} Project')
        self.assertEqual(entry.data['publisher'], 'IEEE')

    def test_concatenation_and_quoted_value(self):
        entry = self.by_key['concat']
        self.assertEqual(entry.data['title'], 'Hello World')
        self.assertEqual(entry.data['booktitle'], 'Conference on {Things}')

    def test_parenthesis_delimiters(self):
        entry = self.by_key['paren-key']
        self.assertEqual(entry.data['title'], 'Parentheses work')

    def test_crossref_fills_missing_fields(self):
        child = self.by_key['child']
        self.assertEqual(child.data['booktitle'], 'ICSE')
        self.assertEqual(child.data['year'], '2011')
        self.assertEqual(child.data['title'], 'A paper')

    def test_recovers_after_broken_entry(self):
        self.assertIn('recovered', self.by_key)
        self.assertEqual(self.by_key['recovered'].data['title'],
                         'Still parsed after a broken neighbour')

    def test_authors_helper(self):
        self.assertEqual(
            self.by_key['multiline'].authors(),
            ['Jane Doe', 'John Smith'],
        )

    def test_search_includes_key_and_fields(self):
        self.assertTrue(self.by_key['braces'].search(['gnu']))
        self.assertTrue(self.by_key['concat'].search(['lovelace']))
        self.assertTrue(self.by_key['paren-key'].search(['paren-key']))

    def test_empty_input(self):
        self.assertEqual(bibparse.parse_string(''), [])
        self.assertEqual(bibparse.parse_string('   % just a comment\n'), [])

    def test_inline_comments_and_extra_strings(self):
        text = """
        @misc{x,
          % comment between fields
          title = {Y},
          publisher = acm
        }
        """
        entries = bibparse.parse_string(text, strings={'acm': 'ACM Press'})
        self.assertEqual(entries[0].data['title'], 'Y')
        self.assertEqual(entries[0].data['publisher'], 'ACM Press')

    def test_export_keeps_inner_braces(self):
        rendered = self.by_key['braces'].export()
        self.assertIn('The {GNU} Project', rendered)
        self.assertIn('@book{braces,', rendered)


class ParseFileTests(unittest.TestCase):
    def test_parse_bib_utf8_and_roundtrip_api(self):
        text = '@misc{naïve, title = {Café}, year = 2024}\n'
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'sample.bib')
            with open(path, 'w', encoding='utf-8') as handle:
                handle.write(text)
            entries = bibparse.parse_bib(path)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].key, 'naïve')
            self.assertEqual(entries[0].data['title'], 'Café')
            self.assertEqual(entries[0].data['filename'], path)
            via_parse = bibparse.parse(path)
            self.assertEqual(via_parse[0].key, 'naïve')

    def test_parse_accepts_string_content(self):
        entries = bibparse.parse('@misc{x, title={Y}}')
        self.assertEqual(entries[0].key, 'x')
        self.assertEqual(entries[0].data['title'], 'Y')

    def test_existing_workspace_bib(self):
        path = os.path.join(
            os.path.dirname(__file__),
            '..', '..', 'the-wartime-cto-book', 'references.bib',
        )
        path = os.path.abspath(path)
        if not os.path.isfile(path):
            self.skipTest('workspace references.bib not present')
        entries = bibparse.parse_bib(path)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].key, 'example_reference')
        self.assertEqual(entries[0].btype.lower(), 'book')
        self.assertIn('Mythical Man-Month', entries[0].data['title'])


class ValidatorTests(unittest.TestCase):
    def test_article_required_fields(self):
        entries = bibparse.parse_string(
            '@article{ok, title={T}, author={A}, journal={J}, year=2020}'
        )
        self.assertTrue(BibFields.validate_entry(entries[0]))
        incomplete = bibparse.parse_string('@article{bad, title={T}}')
        self.assertFalse(BibFields.validate_entry(incomplete[0]))

    def test_book_accepts_editor_instead_of_author(self):
        entries = bibparse.parse_string(
            '@book{ok, title={T}, editor={E}, year=1999, publisher={P}}'
        )
        self.assertTrue(BibFields.validate_entry(entries[0]))


class TemplateTests(unittest.TestCase):
    def test_new_entry(self):
        text = bibparse.BibtexEntry.new_entry('article')
        self.assertIn('@Article', text)
        self.assertEqual(
            bibparse.BibtexEntry.new_entry('nope'),
            'Invalid type: nope',
        )


if __name__ == '__main__':
    unittest.main()
