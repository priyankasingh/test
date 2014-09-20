#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import MySQLdb
from BeautifulSoup import BeautifulSoup
from time import sleep

def keep_log(str):
	str = str.encode('utf-8')
	file = open("sof_question_log.txt","a")
	file.write(str)
	file.write("\n")
	file.close()

db =  MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Southampton11",
        db="Test")

cursor = db.cursor()

query = """SELECT tag_url FROM sof_tag LIMIT 10;"""

try:
	cursor.execute(query)
	numrows = int(cursor.rowcount)

	rows = cursor.fetchall()
	tag_name= rows[0]
	keep_log(tag_name)

	for i in range (numrows):
#		row = cursor.fetchone()
		keep_log('Tag used:' + rows[i][0])
		base_url = rows[i][0]   # Problem solved
		program_url = base_url + "?sort=votes&pagesize=50"
		
#		print program_url
		keep_log(program_url)
		soup = BeautifulSoup(urllib2.urlopen(program_url))

		for page in soup.findAll("span",{'class': 'page-numbers'}):
			a = page.string
		
		keep_log('No of pages:' + a)	

#		pages = range(1, int(a) + 1)
		pages = range(1, 4)
		for p in pages:	
			url = '%s&page=%s' % (program_url,p)
#			print url
			keep_log(url)
				
			soup2 = BeautifulSoup(urllib2.urlopen(url))
			sleep(10)

			for link in soup2.findAll("a",{'class' : 'question-hyperlink'}):
				tag_url = base_url + link.get('href')
				tag = link.string
				
				query2 = """INSERT IGNORE INTO sof_question 
					(question, question_url, created_date, modified_date) 
                        		VALUES ('%s', '%s', NOW(), NOW())
					ON DUPLICATE KEY UPDATE modified_date = NOW();
					""" % (tag, tag_url)
				
				try:

					cursor.execute(query2)
        	                	db.commit()
#					print "Insert Successful"

				except:
					pass
#				print tag.encode('utf-8') , tag_url	


except (ValueError) as e:
	print e
