
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
    
    @staticmethod
    def validate_entry(bibentry):
        return False
                
    