from datetime import datetime
import logging
import pytz
import re

import reddit
import solr

logging.basicConfig(filename='logs/gather.log', level=logging.INFO)

solr = solr.SolrConnection('http://localhost:8983/solr')
reddit = reddit.Reddit(user_agent='occupymanifesto')
subreddit = reddit.get_subreddit('occupymanifesto')

nodes = []
for item in subreddit.get_hot(limit=None):

	logging.info('Processing {%s}' % item)

	# Only process submissions which have a valid noun-phrase type
	type = None
	matches = re.match('(.*):', item.title)
	if not matches:
		logging.info('Skipping {%s} since it has no noun-phrase type specified' % item)
		continue

	# Only text submissions are currently considered for visualization
	if not item.__dict__.has_key('selftext'):
		logging.info('Skipping {%s} since it does not contain a selftext field' % item)
		continue

	type = matches.group(1).strip()

	# Link this item to any existing parent
	parent = None
	parent_path = None
	for line in item.selftext.splitlines():

		# Scan the message line-by-line looking for parent identifiers
		matches = re.match('parent:(.*)', line)
		if not matches:
			continue

		# Extract the parent item ID
		parent_url = matches.group(1).strip()
		matches_long = re.match('(http.?://.*reddit.com)(/r/)(.*)(/comments/)(.*)(/.*/)', parent_url)
		matches_short = re.match('(http.?://.*redd.it)(/)(.*)', parent_url)

		if matches_long:
			parent = matches_long.group(5)
		elif matches_short:
			parent = matches_short.group(3)
		else:
			continue

		# Extract the parent document's full path
		parent_path = None
		response = solr.query('id:%s' % parent)
		if response.results and response.results[0].has_key('path'):
			parent_path = response.results[0]['path'] 
			break

	# Build up this item's path
	path = (parent_path or '') + '/' + item.id
	logging.info('Constructed path %s for {%s}' % (path, item))

	# Prepare a document to be loaded into Solr
	node = {
		'datetime': datetime.fromtimestamp(item.created_utc, pytz.UTC),

		'id': item.id,
		'type': type,
		'path': path,
		'parent': parent,

		'points': item.score,
		'title': item.title.encode('utf-8')
	}
	nodes.append(node)

# Load documents into Solr and commit the changes
solr.add_many(nodes)
solr.commit()
solr.close()
