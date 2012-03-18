from cStringIO import StringIO

class TextFormatter:
	def __init__(self, bibentry):
		self.bibentry = bibentry
		self.fmethods = {}
		self.fmethods['article'] = __article	
		return
		
	def export(self):
		return self.fmethods[self.bibentry.btype.lower()]()
	
	def __get(self, key, error):
		try:
			return self.bibentry.data[key].trim()
		except KeyError:
			return error
	
	def __article(self):
		# AuthorName(s). Journal article. Journal, VolumeNumber(Number):Pages, Month Year. Note.
		return "%s, %s, %s, %s, %s(%s):%s, %s, %s"

#@Article{
#@Book{
#@Booklet{
#@InBook{
#@InCollection{
#@InProceedings{
#@Manual{
#@MastersThesis{
#@Misc{
#@PhDThesis{
#@Proceedings{
#@TechReport{
#@Unpublished{
