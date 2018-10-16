import matplotlib.pyplot as plt
import sys
import math

def plot_zipf(ngram_probs):
	sorted_ngram_probs = sorted(ngram_probs.items(), key = lambda x: x[1], reverse=True)
	print sorted_ngram_probs[:100]
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

def get_laplace_probs(n, ngrams, n_minus1_grams, V):
	ngram_probs = {}
	N = 0
	if n == 1:
		N = n_minus1_grams
	for ngram in ngrams:
		if n != 1:
			ngram_probs[ngram] = ((ngrams[ngram] + 1) * 1.0)/(n_minus1_grams[ngram[:(n - 1)]] + V)
		else:
			ngram_probs[ngram] = ((ngrams[ngram] + 1) * 1.0)/(N + V)

	return ngram_probs	

if sys.argv[1] == "1":
	unigrams, N, V = get_ngrams(1, "./tokenized")
	unigram_probs = get_laplace_probs(1, unigrams, N, V)
	plot_zipf(unigram_probs)

elif sys.argv[1] == "2":
	bigrams, N, V = get_ngrams(2, "./tokenized")
	unigrams, N, V = get_ngrams(1, "./tokenized")
	bigram_probs = get_laplace_probs(2, bigrams, unigrams, V)
	plot_zipf(bigram_probs)	

elif sys.argv[1] == "3":
	trigrams, N, V = get_ngrams(3, "./tokenized")
	bigrams, N, V = get_ngrams(2, "./tokenized")
	trigrams_probs = get_laplace_probs(3, trigrams, bigrams, V)
	plot_zipf(trigrams_probs)