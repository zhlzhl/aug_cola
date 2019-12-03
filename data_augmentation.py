import random
from random import shuffle
from token_utils import tokenize, untokenize
# for the first time you use wordnet
# import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.corpus import wordnet
import spacy


def get_synonyms(word, pos):
    pos_map = {"ADJ": 'a',
               "ADJ_SAT": 's',
               "ADV": 'r',
               "NOUN": 'n',
               "VERB": 'v'}

    synonyms = set()
    for syn in wordnet.synsets(word, pos=pos_map[pos]):
        for l in syn.lemmas():
            synonym = l.name().replace("_", " ").replace("-", " ").lower()
            synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
            synonyms.add(synonym)
    if word in synonyms:
        synonyms.remove(word)
    return list(synonyms)


def replace(sentence, the_word, synonym):
    tokens = tokenize(sentence)
    # replace the_word with synonym
    try:
        assert the_word in tokens
    except AssertionError:
        print("AssertionError")
        print("sentence: {}\nthe world: {}\nsynonym: {}".format(sentence, the_word, synonym))
        return None

    new_tokens = [synonym if word == the_word else word for word in tokens]
    new_sentence = untokenize(new_tokens)

    # print("--old: ", sentence)
    # print("replaced", the_word, "with", synonym)
    # print("--new: ", new_sentence)

    return new_sentence


def synonym_replacement(sentence, words_to_replace, num_sr_words):
    random_word_list = words_to_replace.copy()
    random.shuffle(random_word_list)

    new_sentence = None
    # randomly select a word from the word_to_replace, and replace it with its synonym
    num_replaced_words = 0
    for random_word, pos in random_word_list:
        synonyms = get_synonyms(random_word, pos)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_sentence = replace(sentence, random_word, synonym)

            if new_sentence is not None and new_sentence != sentence:
                sentence = new_sentence
                num_replaced_words += 1

        if num_replaced_words >= num_sr_words:  # only replace up to n_sr words
            break

    return new_sentence


import random


## randomly swap two words in a sentence
def random_swap(sentence, distance=1):
    """
    randomly swap words in a sentence
    :params[in]: sentence, a string, input sentence
    :params[in]: distance, integer, distance of words

    :params[out]: n_sentence, a string, new sentence
    """
    # lis = sent.split(' ')  # split by spaces
    tokens = tokenize(sentence)
    tokens_length = len(tokens)
    assert tokens_length >= 2
    index1 = random.randint(0, tokens_length - 1)
    # canidates pool
    candidates = set(range(index1 - distance, index1 + distance + 1)) & set(range(tokens_length))
    candidates.remove(index1)
    # randomly sample another index
    index2 = random.sample(candidates, 1)[0]
    # swap two elements
    tokens[index1], tokens[index2] = tokens[index2], tokens[index1]
    # n_sen = ' '.join(lis)
    n_sentence = untokenize(tokens)
    # return new sentence
    return n_sentence


def random_deletion(sentence, n=1):
    tokens = tokenize(sentence)

    # obviously, if there's only one word, don't delete it
    if len(tokens) == 1:
        return tokens

    # randomly delete upto n words
    count = 0
    while count < n:
        assert n < len(tokens)
        rand_index = random.randint(0, len(tokens) - 1)
        del tokens[rand_index]
        count += 1

    return untokenize(tokens)

# TODO:there is a bug delete_pos method, and needs to be further investigated.
# def delete_pos(sentence, pos):
#     nlp = spacy.load("en_core_web_sm")
#     tokens = nlp(sentence)
#
#     # get verbs and nouns
#     print(len(tokens))
#     print(range(len(tokens)))
#     print(zip(range(len(tokens)), tokens))
#     for i, token in zip(range(len(tokens), tokens)):
#         print("{}, {}".format(i, token.text, token.pos_))
#     index_of_words_to_delete = [i for i, token in zip(range(len(tokens), tokens)) if token.pos_ in pos]
#
#     # obviously, if there's only one word, don't delete it
#     if len(tokens) == 1:
#         return tokens[0].text
#
#     # delete words of pos
#     del tokens[index_of_words_to_delete]
#
#     return untokenize([token.text for token in tokens])


if __name__ == "__main__":
    sentence = "I'd like to know when he's coming."

    # print(sentence)
    # new_sentence = delete_pos(sentence, "ADP")
    # print(new_sentence)
