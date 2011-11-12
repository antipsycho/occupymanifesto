from datetime import datetime
import pytz
import re

import reddit
import solr

reddit = reddit.Reddit(user_agent='occupymanifesto')
subreddit = reddit.get_subreddit('occupymanifesto')

nodes = []
for item in subreddit.get_hot(limit=None):

	matches = re.match('(.*):', item.title)

	if not matches or not matches.group(1) in ('Principle', 'Rationale', 'Evidence'):
		continue

	node = {
		'id': item.id,
		'type': matches.group(1),
		'title': item.title.encode('utf-8'),
		'datetime': datetime.fromtimestamp(item.created_utc, pytz.UTC),
		'points': item.score
	}
	nodes.append(node)

solr = solr.SolrConnection('http://localhost:8983/solr')
solr.add_many(nodes)
solr.commit()
solr.close()
