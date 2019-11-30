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
1. An augmented sentence is created by replacing words in the original sentence with synonyms. The original sentence is tokenized to be worked on. The challenge is, after tokenization, the sentence is separated to a list of tokens, and when joining these tokens with ' ' (space), a space is also added in front of puntuations. This could lead to poor performance of the generated cola dataset, as CoLA is to check for grammaer correctness. 


2. synonyms are queried from wordnet.synsets(word, pos=pos_map[pos]). I assume this method is based on word embeddings from wordnet. 

3. Didn't create a dictionary of all words in the dataset. Not sure how is this needed. 
