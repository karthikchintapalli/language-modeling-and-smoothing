special_chars = ['/', '.', '(', ')', '[', ']', '?', ' ', ':']
with open('./tagged', 'r') as f, open('./iob_tagged', 'w+') as g:
	for sentence in f:
		tags = []
		for c in sentence.strip('\n'):
			if c in special_chars:
				tags.append('O')
			else:
				tags.append('I')
		g.write(''.join(tags) + '\n')
