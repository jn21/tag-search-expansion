from whoosh.index import open_dir
from whoosh import query,writing
import argparse
import sqlite3
import time

def indexTweets(db_name):
    """Retrieve all documents index them using Whoosh."""
    
    index = open_dir("index")
    
    print "Indexing process beginning at ", time.strftime("%H:%M:%S")
    
    #Get tweets from DB
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute('''SELECT msg,hashtags FROM hashed_tweets''')
    all_rows = cursor.fetchall()
      
    print "Documents retrieved from database. Adding new documents to index..." 
    
    #Add tweets to index
    writer = index.writer(limitmb=256)
    for i in range(len(all_rows)):
        writer.add_document(content=all_rows[i][0],tags=all_rows[i][1])
        
    print "%d new documents added to index. Committing changes..." % len(all_rows)
    
    #commit changes
    writer.commit()
    
    print "Changes committed."
    print "Indexing process finished at ", time.strftime("%H:%M:%S")
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("db_name", help="(Required) Name of database to find tweets from")
    args = parser.parse_args()
    db_name = args.db_name

    indexTweets(db_name)