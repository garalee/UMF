import UMF_Indexer

if __name__ == "__main__":
    indexer = UMF_Indexer.UMF_Indexer()

    urlList = indexer.extractDocumentUrl('data')
    print urlList
