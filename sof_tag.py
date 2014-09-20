#!/usr/bin/python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import re
import urllib2
import MySQLdb

db =  MySQLdb.connect(
	host="localhost", 
	user="root", 
	passwd="Southampton11", 
	db="Test")

cursor = db.cursor()

base_url = "http://stackoverflow.com"
program_url = base_url + "/tags?page="


for page in range(1,893):
	url = "%s%d" % (program_url, page)
	soup = BeautifulSoup(urllib2.urlopen(url))
	
	for link in soup.findAll("a",{'class' : 'post-tag'}):
		tag_url = base_url + link.get('href')
		tag = link.string
		#print tag, tag_url
		
		query = """INSERT INTO sof_tag (tag, tag_url) 
			VALUES ('%s', '%s');
			""" % (tag, tag_url)
	
		try:
			cursor.execute(query)
			db.commit()
			
		except (ValueError) as e:
			print e
#			db.rollback()
#			db.close()

#db.close()
