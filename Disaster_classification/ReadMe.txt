Disaster classification
The provided dataset being rather small for neural network training, creating a NN from scratch, i.e. a simple LSTM encoder decoder, resulted in a low accuracy and a very quick overfitting.
Therefore we chose to use a pretrained distilbert (lighter and faster BERT) Model from huggingface.
pretreatment: decode html character, decode all accents with unidecode library, replace urls with "URL" , "&" wit "and", delete most non-digits, non-letters characters, except some that, we found, improve the results of the model (namely # and .).

This resulted in an accuracy for the validation set of ~0.84