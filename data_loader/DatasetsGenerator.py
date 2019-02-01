import csv
import os
import numpy as numpy
from bs4 import BeautifulSoup
from requests import get
import lxml
from multiprocessing import Process, Pool
def getname(line):
	"""
	Deciphers and parses the name of a player given a line from a file within
	./data_loader/data/early_applicants/txt
	"""
	parts = line.replace('\n', '').replace('|', ',').split(',')
	fullname = parts[0]
	split_name = fullname.split(' ')
	firstname = split_name[0]
	lastname = ' '.join(split_name[1:])
	return firstname, lastname


def early_applicants_txt2csv():
	"""
	Some of the nba early_applicant website formats are difficult to webscrape, so assuming
	we have the directory ./data_loader/data/early_applicants/txt which has a handful of
	txt files containing pasted content from the site, we will generate csv files
	of those players.
	"""
	rootdir = './data_loader/data/early_applicants/txt'
	filenames = os.listdir(rootdir)
	filenames = [os.path.join(rootdir, filename) for filename in filenames]

	for filename in filenames:
		data = []
		with open(filename, 'r') as file:
			with open(filename.replace('txt', 'csv'), 'w') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(['first_name', 'last_name'])
				line = file.readline()
				while line:
					writer.writerow(getname(line))
					line = file.readline()


def get_year_csv(args):
	"""
	Generates the year csv given some url to web scrape and the year you want to scrape on.
	Used to generate the early_applicants csv validation file
	"""
	url, year = args
	content = get(url).content
	soup = BeautifulSoup(content, 'lxml')
	table = soup.findAll('table')[1]
	players = table.findAll('tr')
	with open('./data_loader/data/early_applicants/csv/{0}.csv'.format(year), 'w') as csvfile:
		writer = csv.writer(csvfile)
		for i, player in enumerate(players):
			if (i == 0):
				writer.writerow(['first_name', 'last_name'])
			else:
				name = player.find('td').getText().strip().split(' ')
				first_name = name[0]
				last_name = ' '.join(name[1:])
				writer.writerow([first_name, last_name])


def get_nba_data(soup):
	"""
	Given some soup object, parses and returns nba player information. Used when 
	generating draftpick data

	@param soup: BeautifulSoup object of a table row
	"""
	player = soup.find('td', {'class':'player'}).getText()
	team = soup.find('td', {'class':'team'}).getText()
	affiliation = soup.find('td', {'class':'first text'}).getText()
	year, num, pick, overrall = soup.findAll('td', {'class':''})
	return [player, team, affiliation, year.getText(), num.getText(), pick.getText(),
	        overrall.getText()]


def nba_draftpicks():
	"""
	Generates nba draftpicks using pasted html source code inside the directory
	./data_loader/data/draftpicks/html
	"""
	url = 'https://stats.nba.com/draft/history/?Season='
	html_rootdir = './data_loader/data/draftpicks/html'
	csv_rootdir = './data_loader/data/draftpicks/csv'

	raw_files = [os.path.join(html_rootdir, filename) for filename in os.listdir(html_rootdir)]
	html_files = []
	for filename in raw_files:
	    with open(filename, 'r') as file:
	        html_files.append(file.read())

	header = ['Player', 'Team', 'Affiliation', 
		'Year', 'Round Number', 'Round Pick', 
		'Overall Pick']

	for i, date in enumerate(os.listdir(html_rootdir)):
		filename = date.replace('.htm', '')
		csv_filepath = os.path.join(csv_rootdir, '{0}.csv'.format(filename))
		with open(csv_filepath, 'w') as csv_file:
		    soup = BeautifulSoup(html_files[i], 'lxml')
		    table = soup.find('table')
		    writer = csv.writer(csv_file)
		    writer.writerow(header)
		    rows = table.findAll('tr')
		    for k, row in enumerate(rows):
		        if k != 0:
		            writer.writerow(get_nba_data(row))


def getall():
	"""
	Generates all custom made datasets
	"""
	args = (
		('http://www.nba.com/2016/news/04/26/early-entry-candidates-2016-draft/', '2016'),
		('http://www.nba.com/2015/news/04/28/early-entry-candidates-for-2015-draft/', '2015')
	)
	pool = Pool()
	pool.map(get_year_csv, args)
	pool.apply(nba_draftpicks)
	pool.apply(early_applicants_txt2csv)
	pool.close()
	pool.join()

if __name__ == '__main__':
	getall()
