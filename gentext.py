import sys
import math
import matplotlib.pyplot as plt
import random

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

def P_KN_lower(ngram, D):
	if len(ngram) == 2:
		return (max(N_uniq("_", ngram) - D, 0.0) * 1.0)/(N_uniq("_", ngram[: -1],"_")) + D * ((N_uniq(ngram[: -1], "_") * 1.0)/(N_uniq("_", ngram[: -1],"_"))) * P_KN_lower(ngram[1: ], D)

	else:
		return (max(N_uniq("_", ngram) - D, 0.0) * 1.0)/(V_bi) + (D/V_uni)

def P_KN(ngram, D):
	if len(ngram) == 1:
		return P_KN_lower(ngram, D)
	return ((max(counts(ngram) - D, 0.0) * 1.0)/(counts(ngram[: -1]))) + D * ((N_uniq(ngram[: -1], "_") * 1.0)/counts(ngram[: -1])) * P_KN_lower(ngram[1: ], D)

ngrams = [{} for i in xrange(3)]

ngrams[0], N_uni, V_uni = get_ngrams(1, './tokenized')
ngrams[1], N_bi, V_bi = get_ngrams(2, './tokenized')
ngrams[2], N_tri, V_tri = get_ngrams(3, './tokenized')

smoothed_probs = {}
for ngram in ngrams[int(sys.argv[1]) - 1]:
	smoothed_probs[ngram] = P_KN(ngram, 0.75)

sorted_ngram_probs = sorted(smoothed_probs.items(), key = lambda x: x[1], reverse=True)

text = []
if sys.argv[1] == "1":
	i = 0
	while i < 10:
		r = random.random()
		p_mass = 0
		for pair in sorted_ngram_probs:
			p_mass += pair[1]
			if p_mass >= r:
				text.append(pair[0][0])
				break

		i += 1

	print ' '.join(text)

elif sys.argv[1] == "2":
	text.append("the")
	i = 0
	flag = 1
	while i < 10 and flag == 1:
		flag = 0
		r = random.random()
		p_mass = 0
		for pair in sorted_ngram_probs:
			if pair[0][0] == text[i]:
				p_mass += pair[1]
				if p_mass >= r:
					text.append(pair[0][1])
					i += 1
					flag = 1
					break

	print ' '.join(text)

elif sys.argv[1] == "3":
	text.append("the")
	text.append("only")
	i = 1
	flag = 1
	while i < 10 and flag == 1:
		flag = 0
		r = random.random()
		p_mass = 0
		for pair in sorted_ngram_probs:
			if pair[0][0] == text[i - 1] and pair[0][1] == text[i]:
				p_mass += pair[1]
				if p_mass >= r:
					text.append(pair[0][2])
					i += 1
					flag = 1
					break

	print ' '.join(text)