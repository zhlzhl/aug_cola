# augment cola dataset

from data_augmentation import *
import spacy
from pycontractions import Contractions


def augment_sentence(sentence, method, pos=None, num_words=0, num_aug_sentences=9, distance=1, new_label=None):
    # create a list for augmented_sentences and add the original sentence
    augmented_sentences = []

    if method == "SR-POS":
        nlp = spacy.load("en_core_web_sm")
        tokenized_sentence = nlp(sentence)

        # get verbs and nouns
        words_to_replace = [(token.text, token.pos_) for token in tokenized_sentence if token.pos_ in pos]


        count = 0
        while len(augmented_sentences) < num_aug_sentences:
            if count >= 50:  # make sure there is no more than 50 iterations
                break

            new_sentence = synonym_replacement(sentence, nlp, words_to_replace, num_words)
            if new_sentence not in augmented_sentences and new_sentence is not None:
                augmented_sentences.append(new_sentence)

            count += 1

    # generate sentence by random swapping
    elif method == "RS":
        count = 0
        while len(augmented_sentences) < num_aug_sentences:
            if count >= 50:  # make sure there is no more than 50 iterations
                break

            new_sentence = random_swap(sentence, distance=distance)
            if new_sentence not in augmented_sentences and new_sentence is not None:
                augmented_sentences.append(new_sentence)

            count += 1

    # generate sentence by random deletion
    elif method == "RD":
        count = 0
        while len(augmented_sentences) < num_aug_sentences:
            if count >= 50:  # make sure there is no more than 50 iterations
                break

            new_sentence = random_deletion(sentence, n=num_words)
            if new_sentence not in augmented_sentences and new_sentence is not None:
                augmented_sentences.append(new_sentence)

            count += 1

    # TODO: FIX THE BUG IN DROP-POS
    # # generate sentence by drop specified pos
    # elif method == "DROP-POS":
    #     count = 0
    #     while len(augmented_sentences) < num_aug_sentences:
    #         if count >= 50:  # make sure there is no more than 50 iterations
    #             break
    #
    #         new_sentence = delete_pos(sentence, pos)
    #         if new_sentence not in augmented_sentences and new_sentence is not None:
    #             augmented_sentences.append(new_sentence)
    #
    #         count += 1


    # shuffle augmented_sentences
    shuffle(augmented_sentences)

    return augmented_sentences


# augment original data using synonym replacement of words with specified POSs
def augment_file(input, output, method, writer=None, pos=None, num_words=0, num_aug_sentences=9,
                 distance=1, labels=[], new_label=None, include_original=False):

    lines = open(input, 'r').readlines()

    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')
        label = parts[1]  # the second column is label
        sentence = parts[3]  # the fourth column is sentence

        aug_sentences = []

        if method == "SR-POS":
            assert pos is not None
            aug_sentences = augment_sentence(sentence, method, pos=pos,
                                             num_words=num_words,
                                             num_aug_sentences=num_aug_sentences)
        elif method == "RS":
            if label in labels:
                aug_sentences.append(augment_sentence(sentence, method, num_aug_sentences=num_aug_sentences, distance=distance))
                # TODO: CHANGE THE OTHER METHOD TO APPEND TO AUG_SENTENCES TOO

        elif method == "RD":
            if label in labels:
                aug_sentences = augment_sentence(sentence, method,
                                                 num_words=num_words,
                                                 num_aug_sentences=num_aug_sentences,
                                                 distance=distance)

        # TODO: FIX BUG IN DROP-POS
        # elif method == "DROP-POS":
        #     if label in labels:
        #         aug_sentences = augment_sentence(sentence, method,
        #                                          pos=pos,
        #                                          num_aug_sentences=num_aug_sentences,
        #                                          new_label=new_label)

        # write out the original sentence
        if include_original:
            writer.write("{}\t{}\t{}\t{}\n".format(parts[0],
                                                   label, # we assume with a distance 0 swap, positive sentence becomes
                                                   # negative, and negative stays negative
                                                   parts[2],
                                                   sentence))
        # write out the augmented sentences
        for sentence in aug_sentences:
            writer.write("{}\t{}\t{}\t{}\n".format(parts[0],
                                                   '0' , # we assume with a distance 0 swap, positive sentence becomes
                                                   # negative, and negative stays negative
                                                   parts[2],
                                                   sentence))

        if i % 10 == 0:
            print("--processed {} lines".format(i))

    print("generated augmented sentences with synonym replacement for " +
          input + " to " + output + " with num_aug_sentences=" + str(num_aug_sentences))


if __name__ == "__main__":
    input_file = '/home/user/git/nlp_data/glue/data/CoLA_backup/train.tsv'
    output_file = '/home/user/git/nlp_data/glue/data/CoLA/train.tsv'


    # # for testing purpose
    # input_file = '/home/user/git/nlp_data/glue/data/CoLA_backup/train_2lines.tsv'
    # output_file = '/home/user/git/nlp_data/glue/data/CoLA/train_2lines.tsv'

    # when more than one methods are used to augment the input, writer needs to be outside the augment_file function
    # so that multiple calls of this function can all write to the same output.
    writer = open(output_file, 'w')


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


    # # augument negative sentences using random swap, negative --> negative
    augment_file(input_file, output_file, method="RS", writer=writer, num_aug_sentences=2, distance=1, labels=['0'], include_original=True)

    # augment positive sentences of cola using random swap and return negative augmented sentences, positive --> neg
    augment_file(input_file, output_file, method="RS", writer=writer, num_aug_sentences=2, distance=1, labels=['1'])

    # augment negative sentences of cola using random deletion, negative --> negative, positive --> negative
    augment_file(input_file, output_file, method="RD", writer=writer, num_aug_sentences=2, num_words=1, labels=['0', '1'])


    # TODO: there is a bug DROP-POS method, and needs to be further investigated.
    # # drop adverb ADV, positive remains positive
    # augment_file(input_file, output_file, pos=['ADV'], writer=writer, method="DROP-POS", num_aug_sentences=2, num_words=1, labels=['1'], new_label='1')

    # # drop punctuation, positive --> negative
    #
    # # drop article DET (this, an, the, a, ...), positive --> negative
    #
    # # drop conjunction, positive --> negative
    #
    # # drop ADP (to, by, from...), positive --> negative

    writer.close()



