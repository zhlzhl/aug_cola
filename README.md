# aug_cola
Augment BERT datasets, including CoLA, RTE, and STS-B, using synonym replace, random swapping, random deletion, and delete by pos.

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
1. synonyms are queried from wordnet.synsets(word, pos=pos_map[pos]).

2. dataset location in augment_cola.py is hard coded. needs to edit input_file and out_file.

### References 
token_utils.py is from https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py 

