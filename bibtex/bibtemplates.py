
def new_article():
	return """@Article{
	Title="Required",
	Author="Required",
	Journal="Required",
	Volume="Optional",
	Number="Optional",
	Pages="Optional",
	Month="Optional",
	Year="Required",
	URL="Optional",
	Note="Optional"
}"""

def new_book():
	return """@Book{
	Title="Required",
	Edition="Optional",
	Series="Optional",
	Volume="Optional",
	Author="Required or Editor",
	Editor="Required or Author",
	Publisher="Required",
	Address="Optional",
	Month="Optional",
	Year="Required",
	URL="Optional",
	Note="Optional",
	ISBN="Optional"
}
"""

def new_booklet():
	return """@Booklet{
	Address="Optional",
	Author="Optional",
	HowPublished="Optional",
	Key="Optional (needed if no Author)",
	Month="Optional",
	Note="Optional",
	Title="Required",
	Year="Optional",
	URL="Optional"
}"""

def new_inbook():
	return """@InBook{
	Address="Optional",
	Author="Required or Editor",
	Chapter="Required or Pages",
	Edition="Optional",
	Editor="Required or Author",
	Month="Optional",
	Note="Optional",
	Pages="Required or Chapter",
	Publisher="Required",
	Series="Optional",
	Title="Required",
	Volume="Optional",
	Year="Required",
	URL="Optional"
}"""

def new_incollection():
	return """@InCollection{
	Author="Required",
	Title="Required",
	Chapter="Optional",
	Pages="Required",
	Editor="Optional",
	Booktitle="Required",
	Publisher="Required",
	Address="Optional",
	Month="Optional",
	Year="Required",
	URL="Optional",
	Note="Optional"
}"""

def new_inproceedings():
	return """@InProceedings{
	Title="Required",
	Author="Required",
	Booktitle="Required",
	Location="Optional",
	Month="Optional",
	Year="Required",
	Organization="Optional",
	Pages="Optional",
	Editor="Optional",
	Address="Optional",
	Publisher="Optional",
	Note="Optional",
	URL="Optional"
}"""

def new_manual():
	return """@Manual{
	Address="Optional",
	Annote="Annotation",
	Author="Optional",
	Edition="Optional",
	Key="Optional (needed if no Author)",
	Month="Optional",
	Note="Optional",
	Organization="Optional",
	Title="Required",
	Year="Optional",
	URL="Optional"
}"""

def new_mastersthesis():
	return """@MastersThesis{
	Address="Optional",
	Author="Required",
	Month="Optional",
	Note="Optional",
	School="Required",
	Title="Required",
	Year="Required",
	URL="Optional"
}"""

def new_misc():
	return """@Misc{
	Author="Optional",
	HowPublished="Optional",
	Key="Optional (needed if no Author)",
	Month="Optional",
	Note="Optional",
	Title="Optional",
	Year="Optional",
	URL="Optional"
}"""

def new_phdthesis():
	return """@PhDThesis{
	Address="Optional",
	Author="Required",
	Month="Optional",
	Note="Optional",
	School="Required",
	Title="Required",
	Year="Required",
	URL="Optional"
}"""

def new_proceedings():
	return """@Proceedings{
	Title="Required",
	Editor="Optional",
	Note="Optional",
	Organization="Optional",
	Location="Optional",
	Publisher="Optional",
	Month="Optional",
	Year="Required",
	URL="Optional"
}"""

def new_techreport():
	return """@TechReport{
	Author="Required",
	Title="Required",
	Note="Optional",
	Type="Optional",
	Number="Optional",
	Month="Optional",
	Year="Required",
	URL="Optional",
	Institution="Required",
	Address="Optional"
}"""

def new_unpublished():
	return """@Unpublished{
	Author="Required",
	Month="Optional",
	Note="Required",
	Title="Required",
	Year="Optional",
	URL="Optional"
}"""
