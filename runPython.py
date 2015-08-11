import UMF_Indexer
import UMF_Analyzer

if __name__ == "__main__":
    indexer = UMF_Indexer.UMF_Indexer()
    analyzer = UMF_Analyzer.UMF_Analyzer()

    analyzer.calculate_query_similarity('a','b')
