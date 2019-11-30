# aug_cola
augment cola dataset

# Known issues
An augmented sentence is created by replacing words in the original sentence with synonyms. The original sentence is tokenized to be worked on. The challenge is, after tokenization, the sentence is separated to a list of tokens, and when joining these tokens with ' ' (space), a space is also added in front of puntuations. This could lead to poor performance of the generated cola dataset, as CoLA is to check for grammaer correctness. 
