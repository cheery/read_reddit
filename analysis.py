import re, sys, json
from operator import mul
from math import log, exp

# If you like to write blogs, you may want to see if your own title
# passes through your own spam filter.
def main():
    config_path = 'config.json'

    with open('config.json', 'r') as fd:
        config = json.load(fd)

    title = " ".join(sys.argv[1:])
    model = model_from_lists(config.get('categories', [
        'spam.list', 'worthless.list',
        'interesting.list', 'important.list']))
    print u" ".join(
        "%.2f" % score(model, title, i)
        for i in range(len(model[1])))

# This utility you have to import. It can be used to find
# out similar titles and find out the ones that are in the
# wrong category.
def list_out(path_to_list, category, limit=0.5):
    config_path = 'config.json'

    with open('config.json', 'r') as fd:
        config = json.load(fd)

    title = " ".join(sys.argv[1:])
    model = model_from_lists(config.get('categories', [
        'spam.list', 'worthless.list',
        'interesting.list', 'important.list']))

    with open(path_to_list) as fd:
        for message in fd.read().split('\n'):
            if score(model, message, category) >= limit:
                print message
                print u" ".join(
                    "%.2f" % score(model, title, i)
                    for i in range(len(model[1])))

# A naive Bayes classifier.
# The information available for the classifier to do the
# decision is very narrow. It could be expanded by crawling
# the web, but I'll first try to deduce stuff just from the
# titles.

# Some of this code was grabbed from the 'antispam' python module.
TOKENS_RE = re.compile(r"\$?\d*(?:[.,]\d+)+|\w+-\w+|\w+", re.U)
INIT_RATING = 0.4

CATEGORY_SPAM = 0
CATEGORY_WORTHLESS = 1
CATEGORY_INTERESTING = 2
CATEGORY_IMPORTANT   = 3

def model_from_lists(sources):
    model = {}, [0 for name in sources]
    for category, filename in enumerate(sources):
        with open(filename) as fd:
            for message in fd.read().split('\n'):
                train(model, message, category)
    return model

def get_word_list(message):
    word_list = filter(lambda s: len(s) > 2,
        TOKENS_RE.findall(message.lower()))
    # Increases the processing time, but should also help the classifier.
    # This means we are also looking at word transitions rather than plain
    # words when doing the decision.
    duples = []
    for i in range(len(word_list) - 1):
        duples.append((word_list[i], word_list[i+1]))
    triples = []
    for i in range(len(word_list) - 2):
        triples.append((word_list[i], word_list[i+1], word_list[i+2]))
    quads = []
    for i in range(len(word_list) - 3):
        triples.append((word_list[i], word_list[i+1], word_list[i+2], word_list[i+3]))
    return word_list + duples + triples + quads

def train(model, message, category):
    token_table, total_count = model
    total_count[category] += 1
    for word in get_word_list(message):
        if word not in token_table:
            token_table[word] = token = [0 for i in total_count]
        else:
            token = token_table[word]
        token[category] += 1

def score(model, message, category=CATEGORY_SPAM):
    token_table, total_count = model
    hashes = get_word_list(message)
    ratings = 0.0
    #i_ratings = []
    for h in hashes:
        rating = INIT_RATING
        if h in token_table:
            spam_count = token_table[h][category]
            spam_total = total_count[category]
            ham_count = sum(c for i, c in enumerate(token_table[h]) if i != category)
            ham_total = sum(c for i, c in enumerate(total_count) if i != category)
            if spam_count > 0 and ham_count == 0:
                rating = 0.99
            elif spam_count == 0 and ham_count > 0:
                rating = 0.01
            elif spam_total > 0 and ham_total > 0:
                ham_prob = float(ham_count) / float(ham_total)
                spam_prob = float(spam_count) / float(spam_total)
                rating = spam_prob / (ham_prob + spam_prob)
                if rating < 0.01:
                    rating = 0.01
        ratings += log(1.0 - rating) - log(rating)
        #ratings.append(log(1.0 - rating) - log(rating))
        # i_ratings.append(1.0 - rating)
    return 1.0 / (1.0 + exp(ratings))

    #if len(ratings) == 0:
    #    return 0

    #if len(ratings) > 20:
    #    ratings.sort()
    #    ratings = ratings[:10] + ratings[-10:]
    #    i_ratings.sort()
    #    i_ratings = i_ratings[:10] + i_ratings[-10:]
    #product = reduce(mul, ratings)
    #i_product = reduce(mul, i_ratings)
    #return product / (product + i_product)

def is_spam(model, message):
    return score(model, message, CATEGORY_SPAM) > 0.9

def is_worthless(model, message):
    return score(model, message, CATEGORY_WORTHLESS) > 0.9

def is_interesting(model, message):
    return score(model, message, CATEGORY_INTERESTING) > 0.5

def is_important(model, message):
    return score(model, message, CATEGORY_IMPORTANT) > 0.5

if __name__=='__main__':
    main()
