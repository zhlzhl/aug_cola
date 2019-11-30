# augment cola dataset

from eda import *
# import argparse

# ap = argparse.ArgumentParser()
# ap.add_argument("--input", required=False, type=str, help="input file of unaugmented data")
# ap.add_argument("--output", required=False, type=str, help="output file of unaugmented data")
# ap.add_argument("--num_aug", required=False, default=5, type=int,
#                 help="number of augmented sentences per original sentence")
# ap.add_argument("--alpha", required=False, default=0.1, type=float,
#                 help="percent of words in each sentence to be changed")
# args = ap.parse_args()


# augment original data using synonym replacement of words with specified POSs
def augment_file_sr_pos(input_file, output_file, pos, num_sr_words, num_aug_sentences=9):
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

    # augment input file using synonym replacement
    # num_sr_words: the number of words that need to be replace in a sentence to generate a new sentence
    # num_aug_sentences: the number of sentences to be generated through augmentation per each sentence in the dataset
    augment_file_sr_pos(input_file, output_file, pos=["VERB", "NOUN"], num_sr_words=2, num_aug_sentences=6)
