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

def plot_zipf(ngram_probs):
	sorted_ngram_probs = sorted(ngram_probs.items(), key = lambda x: x[1], reverse=True)
	freqs = [x[1] for x in sorted_ngram_probs]

	plt.plot(freqs)
	plt.ylabel('Probabilities')
	plt.show()

def plot_log_log(ngram_probs):
	sorted_ngram_probs = sorted(ngram_probs.items(), key = lambda x: x[1], reverse=True)
	freqs = [x[1] for x in sorted_ngram_probs]
	ranks = range(1, len(freqs) + 1)
	freqs = [math.log(x) for x in freqs]
	ranks = [math.log(x) for x in ranks]
	plt.plot(ranks, freqs)
	plt.ylabel('Probabilities')
	plt.show()	

if sys.argv[1] == "1":
	unigrams, N, V = get_ngrams(1, "./tokenized")
	unigram_probs = get_ngram_probs(1, unigrams, N)
	plot_log_log(unigram_probs)

elif sys.argv[1] == "2":
	unigrams, N, V = get_ngrams(1, "./tokenized")
	bigrams, N, V = get_ngrams(2, "./tokenized")
	bigram_probs = get_ngram_probs(2, bigrams, unigrams)
	plot_log_log(bigram_probs)	

elif sys.argv[1] == "3":
	bigrams, N, V = get_ngrams(2, "./tokenized")
	trigrams, N, V = get_ngrams(3, "./tokenized")
	trigrams_probs = get_ngram_probs(3, trigrams, bigrams)
	plot_log_log(trigrams_probs)