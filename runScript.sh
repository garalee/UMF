# !/bin/bash

umf_query="umf_query"
bm25="bm25";
dfr="dfr";
ib="ib";
lmd="lmd";
lmj="lmj";
tfidf="tfidf";
ngram="ngram";
host="http://localhost:9200";

curl -XPOST ${host}/$umf_query bm25/ -d @setting_bm25_query.json
curl -XPOST ${host}/dfr/ -d @setting_dfr_query.json
curl -XPOST ${host}/$ib/ -d @setting_ib_query.json
curl -XPOST ${host}/$lmd/ -d @setting_lmd_query.json
curl -XPOST ${host}/$lmj/ -d @setting_lmj_query.json
curl -XPOST ${host}/$tfidf/ -d @setting_tfidf_query.json
curl -XPOST ${host}/$ngram/ -d @setting_ngram_query.json


# curl -XPOST ${host}/$bm25E/ -d @setting_BM25.json
# curl -XPOST ${host}/$dfrE/ -d @setting_DFR.json
# curl -XPOST ${host}/$ibE/ -d @setting_IB.json
# curl -XPOST ${host}/$lmdE/ -d @setting_LMD.json
# curl -XPOST ${host}/$lmjE/ -d @setting_LMJ.json
# curl -XPOST ${host}/$tfidfE/ -d @setting_TFIDF.json
# curl -XPOST ${host}/$ngramE/ -d @setting_NGRAM.json
