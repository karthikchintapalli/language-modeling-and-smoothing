import sys
import matplotlib.pyplot as plt
import math

def plot_zipf(ngram_probs):
	sorted_ngram_probs = sorted(ngram_probs.items(), key = lambda x: x[1], reverse=True)
	print sorted_ngram_probs[:100]
	freqs = [x[1] for x in sorted_ngram_probs]

	plt.plot(freqs)
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

def followers(context):
	unique = 0
	total = 0
	for ngram in ngrams[len(context)]:
		if ngram[: -1] == context:
			unique += 1
			total += ngrams[len(context)][ngram]

	return unique, total

def P_MLE(ngram):
	if len(ngram) == 1:
		return (ngrams[len(ngram) - 1][ngram] * 1.0)/(N_uni)

	return (ngrams[len(ngram) - 1][ngram] * 1.0)/(ngrams[len(ngram) - 2][ngram[: -1]])

def P_WB(ngram):
	if len(ngram) >= 2:
		N_uniq, C = followers(ngram[: -1])
		lam = (C * 1.0)/(N_uniq + C)
		return lam * P_MLE(ngram) + (1 - lam) * P_WB(ngram[1 :])
	else:
		lam = (N_uni * 1.0)/(N_uni + V_uni)
		return lam * P_MLE(ngram) + (1 - lam)/(V_uni) 

ngrams = [{} for i in xrange(3)]

ngrams[0], N_uni, V_uni = get_ngrams(1, './tokenized')
ngrams[1], N_bi, V_bi = get_ngrams(2, './tokenized')
ngrams[2], N_tri, V_tri = get_ngrams(3, './tokenized')

smoothed_probs = {}
for ngram in ngrams[int(sys.argv[1]) - 1]:
	smoothed_probs[ngram] = P_WB(ngram)
plot_zipf(smoothed_probs)



