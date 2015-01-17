from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from collections import Counter
import operator
import argparse

def getSimilarTag(user_input):
    """Returns similar and cooccuring tags to user input hashtag."""
    
    index = open_dir("index")
    qp_tag = QueryParser("tags", schema=index.schema)

    #Given a user input tag, search for all documents with this tag in the index. Concatenate these documents into the doc_words variable and store the docnums. Also retrieve all cooccuring tags 
    with index.searcher() as searcher:
        
        tag_query = qp_tag.parse(user_input)
        tag_results = searcher.search(tag_query, limit=None)
        
        num_results = tag_results.scored_length()
        
        doc_words = ''
        hit_doc_nums = []
        hit_tags = []
        
        for r in tag_results:
            doc_words = doc_words + r['content'] + ' '
            hit_doc_nums.append(r.docnum)
            hit_tags.append(str.split(str(r['tags'])))

    #if there were no results return empty
    if num_results == 0:
        return([],[],[])
        
    #cooccur_hashes is a dict holding the hashtags that 
    #cooccur with user_input and their frequency
    hit_tags = sum(hit_tags, [])
    cooccur_tags = Counter(hit_tags)
    
    #Perform 2nd search on the index finding results similar to the first pass
    with index.searcher() as searcher:
        num_key_words = 7
        top_res_num = 150
        
        #Do the 2nd search - filter out results from first search
        doc_filter = set(range(searcher.doc_count_all())) - set(hit_doc_nums)
        results = searcher.more_like(0,'content',text=doc_words,top=top_res_num,numterms=num_key_words,filter=doc_filter)
        
        sim_tags = []
        sim_tags_score = {}
        
        for r in results:
            temp_tags = str.split(str(r['tags']))
            sim_tags.append(temp_tags)
            
            #create dict of scores
            for t in temp_tags:
                if t not in sim_tags_score:
                    sim_tags_score.update({t:r.score})
                else:
                    sim_tags_score.update({t:sim_tags_score[t] + r.score})
  
    sim_tags = sum(sim_tags, [])
    sim_tags = Counter(sim_tags)
    
    return (sim_tags,sim_tags_score,cooccur_tags)
    
def rankSimilarTags(sim_tags,sim_tag_score,cooccur_tags,MAX,user_input):
    '''Outputs a ranking of tags from a set of similar and cooccuring tags'''
    
    MIN_SIM_NEEDED_TO_INCLUDE = 3
    MIN_CO_NEEDED_TO_INCLUDE = 2
    COOCCUR_SCORE = 20
    
    #if the input is empty, the output should be empty
    if sim_tags == [] and cooccur_tags == []:
        return []
    
    #remove hash tags that occur a small number of times
    sim_tags = {tag:count for tag,count in sim_tags.items() if count >= MIN_SIM_NEEDED_TO_INCLUDE}
    cooccur_tags = {tag:count for tag,count in cooccur_tags.items() if count >= MIN_CO_NEEDED_TO_INCLUDE}
      
    scored_tags = {}
    for tag,val in sim_tags.items():
        scored_tags[tag] = sim_tag_score[tag]

    #Merge cooccur hashtags into scored_hashes
    for tag,count in cooccur_tags.items():
        if tag in scored_tags:
            scored_tags.update({tag:scored_tags[tag] + COOCCUR_SCORE*count})
        else:
            scored_tags.update({tag:COOCCUR_SCORE*count})
        
    #Rank all hashtags by their score
    ranked_tags = sorted(scored_tags.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    suggested_tags = [x[0] for x in ranked_tags[0:(MAX+1)]]
    
    #remove user_input from suggestions
    suggested_tags = [t for t in suggested_tags if t != user_input]
    
    return suggested_tags
    
def suggestTag():
    """Returns suggested tags similar to a user input tag"""

    #Parse command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("user_input_tag", help="(Required) User input tag")
    parser.add_argument("--max", default=8, help="Maximum number of similar tags to suggest. Application may return less than this number. Default is 8",type=int)
    parser.add_argument("--filename", default="nofile", help="Name of file to write hash tag reccomendations to. If not provided, reccomendations will print to console.")
    
    args = parser.parse_args()
    user_input = args.user_input_tag
    filename = args.filename
    NUM_SUGGEST = args.max
    
    #run the algorithm
    (sim_tags,sim_tag_score,cooccur_tags) = getSimilarTag(user_input)  
    suggestions = rankSimilarTags(sim_tags,sim_tag_score,cooccur_tags,NUM_SUGGEST,user_input)
    
    for i,tag in enumerate(suggestions):
        print(tag)

    
if __name__ == "__main__":
    suggestTag()