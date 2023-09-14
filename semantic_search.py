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

corpus_embeddings = bi_encoder.encode(list(std_airs), convert_to_tensor=True, show_progress_bar=True)
std_airs = list(std_airs)

# This function will search all wikipedia articles for passages that answer the query
def search_simple(query):
    ##### Semantic Search #####
    # Encode the query using the bi-encoder and find potentially relevant passages
    question_embedding = bi_encoder.encode(query, convert_to_tensor=True)
    #question_embedding = question_embedding.cuda
    hits = util.semantic_search(question_embedding, corpus_embeddings, top_k=top_k)
    hits = hits[0]  # Get the hits for the first query
    res = []
    hits = sorted(hits, key=lambda x: x['score'], reverse=True)
    for hit in hits[0:5]:
        res.append((std_airs[hit['corpus_id']].replace("\n", " "), round(float(hit['score'])*100, 2)))
    return res
