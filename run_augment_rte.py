# augment cola dataset

from data_augmentation import *
import spacy
from pycontractions import Contractions


def augment_sentence(sentence, method, pos=None, num_sr_words=0, num_aug_sentences=9, distance=1):
    # create a list for augmented_sentences and add the original sentence
    augmented_sentences = [sentence]

    if method == "SR-POS":
        nlp = spacy.load("en_core_web_sm")
        tokenized_sentence = nlp(sentence)

        # get verbs and nouns
        words_to_replace = [(token.text, token.pos_) for token in tokenized_sentence if token.pos_ in pos]


        count = 0
        while len(augmented_sentences) < num_aug_sentences + 1:
            if count >= 50:  # make sure there is no more than 50 iterations
                break

            new_sentence = synonym_replacement(sentence, nlp, words_to_replace, num_sr_words)
            if new_sentence not in augmented_sentences and new_sentence is not None:
                augmented_sentences.append(new_sentence)

            count += 1

    # generate sentence by random swapping
    elif method == "RS":
        count = 0
        while len(augmented_sentences) < num_aug_sentences + 1:
            if count >= 50:  # make sure there is no more than 50 iterations
                break

            new_sentence = random_swap(sentence, distance=distance)
            if new_sentence not in augmented_sentences and new_sentence is not None:
                augmented_sentences.append(new_sentence)

            count += 1

    # shuffle augmented_sentences
    shuffle(augmented_sentences)

    return augmented_sentences


# augment original data using synonym replacement of words with specified POSs
def augment_file(input, output, method, pos=None, num_words=0, num_aug_sentences=9, distance=1, labels=[]):

    writer = open(output, 'w')
    lines = open(input, 'r').readlines()
    index = -1 # index is -1 as the first line is header with index -1, the content starts with index 0

    for i, line in enumerate(lines):
        aug_sentences=[]
        parts = line[:-1].split('\t')
        label = parts[3]  # the second column is label
        sentence = parts[1]  # the fourth column is sentence
        if method == "SR-POS":
            assert pos is not None
            aug_sentences = augment_sentence(sentence, method, pos=pos,
                                             num_sr_words=num_words,
                                             num_aug_sentences=num_aug_sentences)
        elif method == "RS":
            if label in labels:
                aug_sentences = augment_sentence(sentence, method, num_aug_sentences=num_aug_sentences, distance=distance)
            else:
                aug_sentences = [sentence] # no change, just write out the original sentence

        for aug_sentence in aug_sentences:
            # new_line = (parts[0] if index == 0 else str(index)) + "\t" + aug_sentence + "\t" + parts[2] + "\t" + label + '\n'
            writer.write("{}\t{}\t{}\t{}\n".format(parts[0] if index == -1 else str(index),
                                                   aug_sentence,
                                                   parts[2],
                                                   label))
            index += 1

        if i % 10 == 0:
            print("--processed {} lines".format(i))

    writer.close()
    print("generated augmented sentences with synonym replacement for " +
          input + " to " + output + " with num_aug_sentences=" + str(num_aug_sentences))


if __name__ == "__main__":
    # for testing purpose
    input_file = '/home/user/git/nlp_data/glue/data/RTE_backup/train.tsv'
    output_file = '/home/user/git/nlp_data/glue/data/RTE/train.tsv'

    # 1. pre-process all sentences with pycontractions:
    # contraction = Contractions(api_key="glove-twitter-100")
    # # contraction.load_models()
    # text = "I'd like to know how I'd done that!"
    # text_expanded = contraction.expand_texts(text, precise=True)
    # print(list(text_expanded))


    # augment input file using synonym replacement
    # num_sr_words: the number of words that need to be replace in a sentence to generate a new sentence
    # num_aug_sentences: the number of sentences to be generated through augmentation per each sentence in the dataset
    # augment_file(input_file, output_file, method="SR-POS", pos=["VERB", "NOUN"], num_words=2, num_aug_sentences=6)


    # augument negative sentences using random swap
    augment_file(input_file, output_file, method="RS", num_aug_sentences=2, distance=1,
                 labels=['entailment', 'not_entailment'])

