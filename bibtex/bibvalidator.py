
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
    VOLUME = "volume"
    PUBLISHER = "publisher"
    ADDRESS = "address"
    ISBN = "isbn"
    HOWPUBLISHED = "howpublished"
    CHAPTER = "chapter"
    EDITION = "edition"
    EDITOR = "editor"
    SERIES = "series"
    BOOKTITLE = "booktitle"
    ORGANIZATION = "organization"
    LOCATION = "location"
    ANNOTE = "annote"
    SCHOOL = "school"
    KEY = "key"
    
    ARTICLE_REQUIRED = [TITLE, AUTHOR, JOURNAL, YEAR]
    BOOK_REQUIRED = [TITLE, AUTHOR, EDITOR, YEAR, PUBLISHER]
    BOOKLET_REQUIRED = [TITLE, KEY, AUTHOR]
    INBOOK_REQUIRED = [TITLE, YEAR, PAGES, AUTHOR, CHAPTER, EDITOR]
    INCOLLECTION_REQUIRED = [TITLE, AUTHOR, BOOKTITLE, PUBLISHER, YEAR, PAGES]
    INPROCEEDINGS_REQUIRED = [TITLE, AUTHOR, BOOKTITLE, YEAR]
    MANUAL_REQUIRED = [TITLE]
    MASTERTHESIS_REQUIRED = [TITLE, SCHOOL, YEAR, AUTHOR]
    MISC_REQUIRED = []
    PHDTHESIS_REQUIRED = [TITLE, AUTHOR, YEAR, SCHOOL]
    PROCEEDINGS_REQUIRED = [TITLE, REQUIRED]
    TECHREPORT_REQUIRED = [TITLE, AUTHOR, YEAR, REQUIRED]
    UNPUBLISHED_REQUIRED = [TITLE, AUTHOR, NOTE]
    
    VALID_TYPES = ['article', 'book', 'booklet', 'inbook', 'incollection', 'inproceedings', 'manual', 'mastersthesis', 'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished']
    
    @staticmethod
    def __get_required(btype):
        __req = {'article': BibFields.ARTICLE_REQUIRED,
                 'book': BibFields.BOOK_REQUIRED,
                 'booklet': BibFields.BOOKLET_REQUIRED,
                 'inbook': BibFields.INBOOK_REQUIRED,
                 'incollection': BibFields.INCOLLECTION_REQUIRED,
                 'inproceedings': BibFields.INPROCEEDINGS_REQUIRED,
                 'manual': BibFields.MANUAL_REQUIRED,
                 'mastersthesis': BibFields.MASTERTHESIS_REQUIRED,
                 'misc': BibFields.MISC_REQUIRED,
                 'phdthesis': BibFields.PHDTHESIS_REQUIRED,
                 'proceedings': BibFields.PROCEEDINGS_REQUIRED,
                 'techreport': BibFields.TECHREPORT_REQUIRED,
                 'unpublished': BibFields.UNPUBLISHED_REQUIRED}
                 
        return __req.get(btype, None)
    
    @staticmethod
    def validate_entry(bibentry):
        if bibentry.btype not in VALID_TYPES:
            return False
        
        key_count = 0
        required_list = BibFields.__get_required(bibentry.btype)
        
        if required_list is None:
            return False
        
        for k in bibentry.keys():
            if k in required_list:
                key_count += 1
        
        return key_count == len(required_list)
