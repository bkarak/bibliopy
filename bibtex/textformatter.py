#!/usr/bin/python

# biblio.py - A simple bibliography management tool

# Copyright (c) 2012, Vassilios Karakoidas (vassilios.karakoidas@gmail.com)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
