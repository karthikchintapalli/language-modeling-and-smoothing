import matplotlib.pyplot as plt
import sys
import math

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

def counts(ngram):
	return ngrams[len(ngram) - 1][ngram]

def N_uniq(arg1, arg2, arg3=""):
	count = 0
	if arg3 != "_":
		if arg1 == "_":
			for ngram in ngrams[len(arg2)]:
				if ngram[1: ] == arg2:
					count += 1

		elif arg2 == "_":
			for ngram in ngrams[len(arg1)]:
				if ngram[: -1] == arg1:
					count += 1	

	else:
		for ngram in ngrams[len(arg2)]:
			if ngram[: -1] == arg2:
				count += N_uniq("_", ngram)

	return count	

def P_KN_lower(ngram):
	if len(ngram) == 2:
		return (max(N_uniq("_", ngram), 0.0) * 1.0)/(N_uniq("_", ngram[: -1],"_")) + 0.75 * ((N_uniq(ngram[: -1], "_") * 1.0)/(N_uniq("_", ngram[: -1],"_"))) * P_KN_lower(ngram[1: ])

	else:
		return (max(N_uniq("_", ngram), 0.0) * 1.0)/(V_bi) + (1.0/V_uni)

def P_KN(ngram):
	if len(ngram) == 1:
		return P_KN_lower(ngram)
	return ((max(counts(ngram), 0.0) * 1.0)/(counts(ngram[: -1]))) + 0.75 * ((N_uniq(ngram[: -1], "_") * 1.0)/counts(ngram[: -1])) * P_KN_lower(ngram[1: ])


ngrams = [{} for i in xrange(3)]

ngrams[0], N_uni, V_uni = get_ngrams(1, './tokenized')
ngrams[1], N_bi, V_bi = get_ngrams(2, './tokenized')
ngrams[2], N_tri, V_tri = get_ngrams(3, './tokenized')
unigram_probs = get_laplace_probs(1, ngrams[0], N_uni, V_uni)
bigram_probs = get_laplace_probs(2, ngrams[1], ngrams[0], V_bi)
trigram_probs = get_laplace_probs(3, ngrams[2], ngrams[1], V_tri)

for ngram in ngrams[0]:
	ngrams[0][ngram] = unigram_probs[ngram] * N_uni

for ngram in ngrams[1]:
	ngrams[1][ngram] = bigram_probs[ngram] * ngrams[0][ngram[: -1]]

for ngram in ngrams[2]:
	ngrams[2][ngram] = trigram_probs[ngram] * ngrams[1][ngram[: -1]]

smoothed_probs = {}
for ngram in ngrams[int(sys.argv[1]) - 1]:
	smoothed_probs[ngram] = P_KN(ngram)
sorted_ngram_probs = sorted(smoothed_probs.items(), key = lambda x: x[1], reverse=True)
print sorted_ngram_probs[:100]
plot_zipf(smoothed_probs)