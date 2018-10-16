import re

tokenizer_re = re.compile("n't|'s|'d|'ll|ca n|http[s]? : //[0-9a-zA-Z\./-]*|[\w]+")
with open('./corpora/news.txt', 'r') as f, open('./news_tokenized', 'w+') as g:
	for line in f:
		tokens = tokenizer_re.findall(line)
		new_tokens = []
		for token in tokens:
			new_token = re.sub('[\./:-]', '', token)
			new_token = re.sub('ca n', 'can', new_token)
			new_tokens.append(new_token)

		new_line = ' '.join(new_tokens)
		g.write(new_line + '\n')