import networkx as nx
import numpy as np

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


class SummaryUsingGooglePageRank():
    def __init__(self, document):
        ''' Contents send directly from server '''
        self.document = document

    def textrank(self):
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.tokenize(self.document)

        bow_matrix = CountVectorizer().fit_transform(sentences)
        normalized = TfidfTransformer().fit_transform(bow_matrix)

        similarity_graph = normalized * normalized.T

        nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
        scores = nx.pagerank(nx_graph)
        return sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)


    def summarize(self):
        '''Main function which deals with summarizing
        the text'''

        #f = open(self.input_file, "r")
        #document = f.read()
        #f.close()

        #f = open(self.output_file, "wb")

        #ranked = self.textrank(document)
        ranked = self.textrank()

        summary = ""
        for i in range(10):
            summary += ranked[i][1]

        print summary
        #f.write(summary)
        return summary
