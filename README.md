_______________________________________________
Tag Recommendation Algorithm
_______________________________________________
TRA is a Python implementation of a query expansion model in the context of tag-based text search.
Suppose we have a body of text documents. Each document is tagged with a list of words which are
representative of the content of the document. Examples include hashtags in a tweet, key words in an
article or academic paper, tags in a Stack Exchange post etc.

Suppose we wish to search for documents concerning a given topic by specifying a tag which
corresponds to this topic. For example, we might be interested in tweets concerning the 2014 NCAA
basketball tournament. A logical choice of hashtag to use for our search would be #ncaatournament.
However, it is likely that there are many tweets whose subject is the NCAA tournament which are not
tagged with #ncaatournament. These tweets probably contain tags related to #ncaatournament such as
#marchmadness, #michigan, #louisville etc. TRA is an algorithm which will attempt to discover these
related tags. With these related tags in hand we can expand our search terms to find more documents
relevant to our original criteria.

_______________________________________________
Requirements
_______________________________________________

1. Python 2.7
2. Python Whoosh module
3. Sqlite3 and sqlite python module

_______________________________________________
Example Usage
_______________________________________________
$ python createIndex.py
$ python indexDocuments.py tweets.db
Indexing process beginning at  11:03:25
Documents retrieved from database. Adding new documents to index...
52228 new documents added to index. Committing changes...
Changes committed.
Indexing process finished at  11:04:23
$ python suggestTag.py '#ncaatournament'
#marchmadness
#ncaamarchmadness2014
#goblue
#trndnl
#wisconsin
#ncaa
#orevswisc
#slu

