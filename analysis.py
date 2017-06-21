import re

# A naive Bayes classifier.
# The information available for the classifier to do the
# decision is very narrow. It could be expanded by crawling
# the web, but I'll first try to deduce stuff just from the
# titles.

# 

# Some of this code was grabbed from the 'antispam' python module.
TOKENS_RE = re.compile(r"\$?\d*(?:[.,]\d+)+|\w+-\w+|\w+", re.U)
INIT_RATING = 0.4

CATEGORY_SPAM = 0
CATEGORY_WORTHLESS = 1
CATEGORY_INTERESTING = 2
CATEGORY_IMPORTANT   = 3

def model_from_lists(sources):
    model = {}, [0, 0, 0, 0]
    for category, filename in enumerate(sources):
        with open(filename) as fd:
            for message in fd.read().split('\n'):
                train(model, message, category)
    return model

def get_word_list(message):
    return filter(lambda s: len(s) > 2,
        TOKENS_RE.findall(message.lower()))

def train(model, message, category):
    token_table, total_count = model
    total_count[category] += 1
    for word in get_word_list(message):
        if word not in token_table:
            token_table[word] = token = [0, 0, 0, 0]
        else:
            token = token_table[word]
        token[category] += 1

def score(model, message, category=CATEGORY_SPAM):
    token_table, total_count = model
    hashes = get_word_list(message)
    ratings = []
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
        ratings.append(rating)
    if len(ratings) == 0:
        return 0
    if len(ratings) > 20:
        ratings.sort()
        ratings = ratings[:10] + ratings[-10:]
    product = 1.0
    alt_product = 1.0
    for r in ratings:
        product *= r
        alt_product *= 1.0 - r
    return product / (product + alt_product)

def is_spam(model, message):
    return score(model, message, CATEGORY_SPAM) > 0.9

def is_worthless(model, message):
    return score(model, message, CATEGORY_WORTHLESS) > 0.9

def is_interesting(model, message):
    return score(model, message, CATEGORY_INTERESTING) > 0.5

def is_important(model, message):
    return score(model, message, CATEGORY_IMPORTANT) > 0.5
