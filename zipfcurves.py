import matplotlib.pyplot as plt
import sys
import math

def get_ngrams(n, corpus):
	ngrams = {}
	N = 0
	V = 0
	with open(corpus, 'r') as f:
		for sentence in f:
			tokens = sentence.strip('\n').split()
			for i in xrange(len(tokens) - (n - 1)):
				ngram = tuple(tokens[i : i + n])
				if ngram in ngrams:
					ngrams[ngram] += 1

				else:
					ngrams[ngram] = 1
					V += 1

				N += 1

	return ngrams, N, V

def get_ngram_probs(n, ngrams, n_minus1_grams):
	ngram_probs = {}
	N = 0
	if n == 1:
		N = n_minus1_grams
	for ngram in ngrams:
		if n != 1:
			ngram_probs[ngram] = (ngrams[ngram] * 1.0)/(n_minus1_grams[ngram[:(n - 1)]])
		else:
			ngram_probs[ngram] = (ngrams[ngram] * 1.0)/(N)	

	return ngram_probs

def plot_zipf(ngram_probs, color):
	sorted_ngram_probs = sorted(ngram_probs.items(), key = lambda x: x[1], reverse=True)
	freqs = [x[1] for x in sorted_ngram_probs]
	plt.plot(freqs, color)

unigrams, N, V = get_ngrams(1, "./anime_tokenized")
unigram_probs = get_ngram_probs(1, unigrams, N)
plot_zipf(unigram_probs, 'r')

unigrams, N, V = get_ngrams(1, "./movies_tokenized")
unigram_probs = get_ngram_probs(1, unigrams, N)
plot_zipf(unigram_probs, 'g')

unigrams, N, V = get_ngrams(1, "./news_tokenized")
unigram_probs = get_ngram_probs(1, unigrams, N)
plot_zipf(unigram_probs, 'b')

plt.ylabel('Probabilities')
plt.show()
