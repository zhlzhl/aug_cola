# augment cola dataset

from data_augmentation import *
import spacy
from pycontractions import Contractions
import nltk

def augment_sentence(sentence, pos, num_sr_words, num_aug_sentences=9):
    nlp = spacy.load("en_core_web_sm")
    tokenized_sentence = nlp(sentence)

    # get verbs and nouns
    words_to_replace = [(token.text, token.pos_) for token in tokenized_sentence if token.pos_ in pos]

    augmented_sentences = []
    # append the original sentence
    augmented_sentences.append(sentence)
    count = 0
    while len(augmented_sentences) < num_aug_sentences + 1:
        if count >= 50:  # make sure there is no more than 50 iterations
            break

        new_sentence = synonym_replacement(sentence, nlp, words_to_replace, num_sr_words)
        if new_sentence not in augmented_sentences and new_sentence is not None:
            augmented_sentences.append(new_sentence)

        count += 1

    shuffle(augmented_sentences)

    return augmented_sentences


# augment original data using synonym replacement of words with specified POSs
def augment_file(input_file, output_file, pos, num_sr_words, num_aug_sentences=9):
    assert pos is not None

    writer = open(output_file, 'w')
    lines = open(input_file, 'r').readlines()

    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')
        label = parts[1]  # the second column is label
        sentence = parts[3]  # the fourth column is sentence
        aug_sentences = augment_sentence(sentence, pos, num_sr_words=num_sr_words, num_aug_sentences=num_aug_sentences)
        for aug_sentence in aug_sentences:
            writer.write(parts[0] + "\t" + label + "\t" + parts[2] + "\t" + aug_sentence + '\n')

        if i % 10 == 0:
            print("--processed {} lines".format(i))

    writer.close()
    print("generated augmented sentences with synonym replacement for " +
          input_file + " to " + output_file + " with num_aug_sentences=" + str(num_aug_sentences)
          + " and num_sr_words={}".format(num_sr_words))


if __name__ == "__main__":
    # for testing purpose
    input_file = '/home/user/git/nlp_data/glue/data/CoLA_backup/train.tsv'
    output_file = '/home/user/git/nlp_data/glue/data/CoLA/train.tsv'

    # 1. pre-process all sentences with pycontractions:
    # contraction = Contractions(api_key="glove-twitter-100")
    # # contraction.load_models()
    # text = "I'd like to know how I'd done that!"
    # text_expanded = contraction.expand_texts(text, precise=True)
    # print(list(text_expanded))


    # augment input file using synonym replacement
    # num_sr_words: the number of words that need to be replace in a sentence to generate a new sentence
    # num_aug_sentences: the number of sentences to be generated through augmentation per each sentence in the dataset
    augment_file(input_file, output_file, pos=["VERB", "NOUN"], num_sr_words=2, num_aug_sentences=6)


    # augument negative sentences using random delete

