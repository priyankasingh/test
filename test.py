#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import MySQLdb
from BeautifulSoup import BeautifulSoup
from MySQLdb import cursors

db =  MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Southampton11",
        db="Test",
	cursorclass = MySQLdb.cursors.SSCursor)

cursor = db.cursor()

query = """SELECT tag_url FROM sof_tag where id=73;"""

try:
        cursor.execute(query)
#        numrows = int(cursor.rowcount)

#       rows = cursor.fetchall()

#       for i in range (numrows):
        row = cursor.fetchone()
        print row[0]
	base_url = row[0]
        program_url = base_url + "?sort=votes&pagesize=50"
		
	soup = BeautifulSoup(urllib2.urlopen(program_url))

        for page in soup.findAll("span",{'class': 'page-numbers'}):
        	a = page.string

	get_question(program_url)

	print a
except:
	pass

def get_question(url):
	print url	
	pages = range(1,4)
	try:

	        for p in pages:
        		page_url = '%s&page=%s' % (url,p)
                	print page_url

                	soup2 = BeautifulSoup(urllib2.urlopen(page_url))

                	for link in soup2.findAll("a",{'class' : 'question-hyperlink'}):
                		tag_url = base_url + link.get('href')
                        	tag = link.string
			
				print tag,tag_url

	except:
		pass

	return
