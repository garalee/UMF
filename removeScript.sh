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


curl -XDELETE ${host}/{$umf_query}_$bm25
curl -XDELETE ${host}/{$umf_query}_$dfr
curl -XDELETE ${host}/{$umf_query}_$ib
curl -XDELETE ${host}/{$umf_query}_$lmd
curl -XDELETE ${host}/{$umf_query}_$lmj
curl -XDELETE ${host}/{$umf_query}_$tfidf
curl -XDELETE ${host}/{$umf_query}_$ngram

curl -XDELETE ${host}/{$umf_document}_$bm25
curl -XDELETE ${host}/{$umf_document}_$dfr
curl -XDELETE ${host}/{$umf_document}_$ib
curl -XDELETE ${host}/{$umf_document}_$lmd
curl -XDELETE ${host}/{$umf_document}_$lmj
curl -XDELETE ${host}/{$umf_document}_$tfidf
curl -XDELETE ${host}/{$umf_document}_$ngram
