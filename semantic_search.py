from config import airs_ref
from sentence_transformers import SentenceTransformer, CrossEncoder, util

std_airs = set()
with open(airs_ref, 'r', encoding="utf8") as afh:
  for line in afh:
    if len(line.strip()) > 0:
      std_airs.add(line.strip())

bi_encoder = SentenceTransformer('distiluse-base-multilingual-cased-v1')
bi_encoder.max_seq_length = 256     #Truncate long passages to 256 tokens
top_k = 32                          #Number of passages we want to retrieve with the bi-encoder

#The bi-encoder will retrieve 100 documents. We use a cross-encoder, to re-rank the results list to improve the quality

#cross_encoder = CrossEncoder('amberoad/bert-multilingual-passage-reranking-msmarco')#
corpus_embeddings = bi_encoder.encode(list(std_airs), convert_to_tensor=True, show_progress_bar=True)
std_airs = list(std_airs)

# This function will search all wikipedia articles for passages that
# answer the query
def search_simple(query):
    #print("Input question:", query)

    ##### BM25 search (lexical search) #####
    #bm25_scores = bm25.get_scores(bm25_tokenizer(query))
    #top_n = np.argpartition(bm25_scores, -5)[-5:]
    #bm25_hits = [{'corpus_id': idx, 'score': bm25_scores[idx]} for idx in top_n]
    #bm25_hits = sorted(bm25_hits, key=lambda x: x['score'], reverse=True)

    #print("Top-3 lexical search (BM25) hits")
    #for hit in bm25_hits[0:5]:
    #    print("\t{:.3f}\t{}".format(hit['score'], std_airs[hit['corpus_id']].replace("\n", " ")))

    ##### Semantic Search #####
    # Encode the query using the bi-encoder and find potentially relevant passages
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    #question_embedding = question_embedding.cuda
    #top_k = 32
    hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]  # Get the hits for the first query

    ##### Re-Ranking #####
    # Now, score all retrieved passages with the cross_encoder
    #cross_inp = [[query, std_airs[hit['corpus_id']]] for hit in hits]
    #cross_scores = cross_encoder.predict(cross_inp)

    # Sort results by the cross-encoder scores
    #for idx in range(len(cross_scores)):
        #hits[idx]['cross-score'] = cross_scores[idx]

    # Output of top-5 hits from bi-encoder
    #print("\n-------------------------\n")
    #print("Top-3 Bi-Encoder Retrieval hits")
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)
    #for hit in hits[0:5]:
        #res.append(std_airs[hit['corpus_id']])
        #print("\t{:.3f}\t{}".format(hit['score'], std_airs[hit['corpus_id']].replace("\n", " ")))
    res = [std_airs[hit['corpus_id']] for hit in hits[0:5]]
    #return std_airs[hits[0]['corpus_id']], std_airs[hits[1]['corpus_id']], std_airs[hits[2]['corpus_id']], std_airs[hits[3]['corpus_id']], std_airs[hits[4]['corpus_id']]
    return res
    # Output of top-5 hits from re-ranker
   # print("\n-------------------------\n")
    #print("Top-3 Cross-Encoder Re-ranker hits")
    #hits = sorted(hits, key=lambda x: x['cross-score'][1], reverse=True)
    #for hit in hits[0:5]:
        #print("\t{:.3f}\t{}".format(hit['cross-score'][1], std_airs[hit['corpus_id']].replace("\n", " ")))
