
import random
from random import shuffle
import spacy

########################################################################
# Synonym replacement
# Replace n words in the sentence with synonyms from wordnet
########################################################################

# for the first time you use wordnet
# import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet


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


def replace(sentence, nlp, the_word, synonym):
    tokenized_sentence = nlp(sentence)
    sentence_words = [token.text for token in tokenized_sentence]

    # replace the_word with synonym
    try:
        assert the_word in sentence_words
    except AssertionError:
        print("AssertionError")
        print("sentence: {}\nthe world: {}\nsynonym: {}".format(sentence, the_word, synonym))
        return None

    new_words = [synonym if word == the_word else word for word in sentence_words]
    new_sentence = ' '.join(new_words)

    # print("--old: ", sentence)
    # print("replaced", the_word, "with", synonym)
    # print("--new: ", new_sentence)

    return new_sentence


def synonym_replacement(sentence, nlp, words_to_replace, num_sr_words):
    random_word_list = words_to_replace.copy()
    random.shuffle(random_word_list)

    new_sentence = None
    # randomly select a word from the word_to_replace, and replace it with its synonym
    num_replaced_words = 0
    for random_word, pos in random_word_list:
        synonyms = get_synonyms(random_word, pos)
        if len(synonyms) >= 1:
            synonym = random.choice(list(synonyms))
            new_sentence = replace(sentence, nlp, random_word, synonym)

            if new_sentence is not None and new_sentence != sentence:
                sentence = new_sentence
                num_replaced_words += 1

        if num_replaced_words >= num_sr_words:  # only replace up to n_sr words
            break

    return new_sentence


def augment_sentence(sentence, pos, num_sr_words, num_aug_sentences=9):
    nlp = spacy.load("en_core_web_sm")
    tokenized_sentence = nlp(sentence)

    # get verbs and nouns
    words_to_replace = [(token.text, token.pos_) for token in tokenized_sentence if token.pos_ in pos]

    augmented_sentences = []
    # append the original sentence
    augmented_sentences.append(sentence)
    count = 0
    while len(augmented_sentences) < num_aug_sentences +1:
        if count >= 50:  # make sure there is no more than 50 iterations
            break

        new_sentence = synonym_replacement(sentence, nlp, words_to_replace, num_sr_words)
        if new_sentence not in augmented_sentences and new_sentence is not None:
            augmented_sentences.append(new_sentence)

        count += 1

    shuffle(augmented_sentences)

    return augmented_sentences


if __name__ == "__main__":
    sentence = "Bill coughed his way out of the restaurant."
    augment_sentences = augment_sentence(sentence, ["VERB", "NOUN"], num_sr_words=2, num_aug_sentences=6)
    print(augment_sentences)