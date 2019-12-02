# aug_cola
augment cola dataset

### Install spacy and wordnet 

Install Spacy
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

Install wordnet
```bash
pip install -U nltk
```
for the first time you use wordnet
```python
import nltk
nltk.download('wordnet')
```

### Known issues

2. synonyms are queried from wordnet.synsets(word, pos=pos_map[pos]). I assume this method is based on word embeddings from wordnet. 

3. Didn't create a dictionary of all words in the dataset. Not sure how is this needed. 

4. dataset location in augment_cola.py is hard coded. needs to edit input_file and out_file.

5. when a word to be replaced occurs more than once in a sentence, all occurences are replaced. Check out the log below
```
AssertionError
sentence: I require to explain exactly why the more you eat , the less you require .
the world: want
synonym: need
```

