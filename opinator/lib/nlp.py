import json
import jsonrpclib

VALUES = {'Neutral': 0, 'Positive': 1, 'Negative': -1, 'Very Negative': -2, 'Very Positive': 2}

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))


def categorize_sentiment(result):
    """Calculates the sum of the sentiments.
        Each type of sentiment is assigned some value
        in the VALUES dictionary
    """
    # print 'result ', result
    # print 'type ', type(result)
    if result[0]['sentiment'] == "Negative":
        return 'Negative'
    elif result[0]['sentiment'] == "Very Negative":
        return 'Very Negative'
    elif result[0]['sentiment'] == "Positive":
        return 'Positive'
    elif result[0]['sentiment'] == "Very Positive":
        return 'Very Positive'
    else:
        return 'Neutral'

def get_sentiment_of_review (review):
    """Calculates the overall sentiment of the reviews"""

    #encoding reviews
    #new_rev = review.encode('utf-8')
    new_rev = review
    #for i in reviews:
        #i.encode('utf-8')
     #   new_rev += i

    #getting the sentiment results
    #from the analyzer module
    nlp = StanfordNLP()
    results = nlp.parse(new_rev)
    result = results['sentences']
    return categorize_sentiment(result)
