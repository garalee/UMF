# !/bin/bash

umf_query="umf_query"
umf_document="umf_document"
bm25="bm25";
dfr="dfr";
ib="ib";
lmd="lmd";
lmj="lmj";
tfidf="tfidf";
ngram="ngram";
host="http://localhost:9200";

curl -XPOST ${host}/{$umf_query}_$bm25/ -d @setting_bm25_query.json
curl -XPOST ${host}/{$umf_query}_$dfr/ -d @setting_dfr_query.json
curl -XPOST ${host}/{$umf_query}_$ib/ -d @setting_ib_query.json
curl -XPOST ${host}/{$umf_query}_$lmd/ -d @setting_lmd_query.json
curl -XPOST ${host}/{$umf_query}_$lmj/ -d @setting_lmj_query.json
curl -XPOST ${host}/{$umf_query}_$tfidf/ -d @setting_tfidf_query.json
curl -XPOST ${host}/{$umf_query}_$ngram/ -d @setting_ngram_query.json

curl -XPOST ${host}/{$umf_document}_$bm25/ -d @setting_bm25_document.json
curl -XPOST ${host}/{$umf_document}_$dfr/ -d @setting_dfr_document.json
curl -XPOST ${host}/{$umf_document}_$ib/ -d @setting_ib_document.json
curl -XPOST ${host}/{$umf_document}_$lmd/ -d @setting_lmd_document.json
curl -XPOST ${host}/{$umf_document}_$lmj/ -d @setting_lmj_document.json
curl -XPOST ${host}/{$umf_document}_$tfidf/ -d @setting_tfidf_document.json
curl -XPOST ${host}/{$umf_document}_$ngram/ -d @setting_ngram_document.json
