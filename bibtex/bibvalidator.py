class BibFields(object):
    TITLE = "title"
    AUTHOR = "author"
    JOURNAL = "journal"
    VOLUME = "volume"
    NUMBER = "number"
    PAGES = "pages"
    MONTH = "month"
    YEAR = "year"
    URL = "url"
    NOTE = "note"
    EDITION = "edition"
    SERIES = "series"
    PUBLISHER = "publisher"
    ADDRESS = "address"
    ISBN = "isbn"
    HOWPUBLISHED = "howpublished"
    CHAPTER = "chapter"
    EDITOR = "editor"
    BOOKTITLE = "booktitle"
    ORGANIZATION = "organization"
    LOCATION = "location"
    ANNOTE = "annote"
    SCHOOL = "school"
    KEY = "key"
    INSTITUTION = "institution"

    ARTICLE_REQUIRED = [TITLE, AUTHOR, JOURNAL, YEAR]
    BOOK_REQUIRED = [TITLE, YEAR, PUBLISHER]
    BOOK_ONE_OF = ([AUTHOR, EDITOR],)
    BOOKLET_REQUIRED = [TITLE]
    INBOOK_REQUIRED = [TITLE, YEAR, PUBLISHER]
    INBOOK_ONE_OF = ([AUTHOR, EDITOR], [CHAPTER, PAGES])
    INCOLLECTION_REQUIRED = [TITLE, AUTHOR, BOOKTITLE, PUBLISHER, YEAR]
    INPROCEEDINGS_REQUIRED = [TITLE, AUTHOR, BOOKTITLE, YEAR]
    MANUAL_REQUIRED = [TITLE]
    MASTERTHESIS_REQUIRED = [TITLE, SCHOOL, YEAR, AUTHOR]
    MISC_REQUIRED = []
    PHDTHESIS_REQUIRED = [TITLE, AUTHOR, YEAR, SCHOOL]
    PROCEEDINGS_REQUIRED = [TITLE, YEAR]
    TECHREPORT_REQUIRED = [TITLE, AUTHOR, YEAR, INSTITUTION]
    UNPUBLISHED_REQUIRED = [TITLE, AUTHOR, NOTE]

    VALID_TYPES = [
        'article', 'book', 'booklet', 'inbook', 'incollection',
        'inproceedings', 'manual', 'mastersthesis', 'misc', 'phdthesis',
        'proceedings', 'techreport', 'unpublished',
    ]

    @staticmethod
    def __get_required(btype):
        required = {
            'article': (BibFields.ARTICLE_REQUIRED, ()),
            'book': (BibFields.BOOK_REQUIRED, BibFields.BOOK_ONE_OF),
            'booklet': (BibFields.BOOKLET_REQUIRED, ()),
            'inbook': (BibFields.INBOOK_REQUIRED, BibFields.INBOOK_ONE_OF),
            'incollection': (BibFields.INCOLLECTION_REQUIRED, ()),
            'inproceedings': (BibFields.INPROCEEDINGS_REQUIRED, ()),
            'manual': (BibFields.MANUAL_REQUIRED, ()),
            'mastersthesis': (BibFields.MASTERTHESIS_REQUIRED, ()),
            'misc': (BibFields.MISC_REQUIRED, ()),
            'phdthesis': (BibFields.PHDTHESIS_REQUIRED, ()),
            'proceedings': (BibFields.PROCEEDINGS_REQUIRED, ()),
            'techreport': (BibFields.TECHREPORT_REQUIRED, ()),
            'unpublished': (BibFields.UNPUBLISHED_REQUIRED, ()),
        }
        return required.get(btype.lower(), None)

    @staticmethod
    def validate_entry(bibentry):
        btype = (bibentry.btype or '').lower()
        if btype not in BibFields.VALID_TYPES:
            return False

        spec = BibFields.__get_required(btype)
        if spec is None:
            return False

        required, alternatives = spec
        present = {k.lower() for k in bibentry.keys()}

        for field in required:
            if field not in present:
                return False

        for group in alternatives:
            if not any(field in present for field in group):
                return False

        return True
