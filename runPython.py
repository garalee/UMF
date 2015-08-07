import UMF_Indexer

if __name__ == "__main__":
    indexer = UMF_Indexer.UMF_Indexer()

    urlList = indexer.extractDocumentUrl('data')
    
    print len(urlList)
    for url in urlList:
        if ('http' in url) or ('https' in url):
            print "URL:",url
            print indexer.getDocumentFromURL(url)

