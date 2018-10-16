def find_tokens(sent):
	tag_seq = []
	chars = [c for c in sent]
	for c in sent:
		tag = 'I'
		Iprod = 1
		if (c, tag) in char_tag_pairs:
			Iprod *= char_tag_pairs[(c, tag)]
		else:
			Iprod = 0
		Iprod = (Iprod * 1.0)/N

		tag = 'O'
		Oprod = 1
		if (c, tag) in char_tag_pairs:
			Oprod *= char_tag_pairs[(c, tag)]
		else:
			Oprod = 0
		Oprod = (Oprod * 1.0)/N

		if Iprod > Oprod:
			tag_seq.append('I')
		else:
			tag_seq.append('O')

	tokens = []
	token = ''
	for i in xrange(len(tag_seq)):
		if tag_seq[i] == 'I':
			token += chars[i]
		else:
			if len(token) > 0:
				tokens.append(token)
			token = ''
	return tokens

char_tag_pairs = {}
N = 0
with open('./tagged', 'r') as f, open('./iob_tagged', 'r') as g:
	line1 = f.read()
	line1 = line1.strip('\n')
	line2 = g.read()
	line2 = line2.strip('\n')
	while line1:	
		chars = [c for c in line1]
		tags = [t for t in line2]

		for c, t in zip(chars, tags):
			if (c, t) in char_tag_pairs:
				char_tag_pairs[(c, t)] += 1
			else:
				char_tag_pairs[(c, t)] = 1
			N += 1

		line1 = f.read()
		line1 = line1.strip('\n')
		line2 = g.read()
		line2 = line2.strip('\n')

sent = "because she 's the worst . i am referring to [ this ] ( http : //i.imgur.com/5srylmi.jpg ) does it have any deeper meaning or does it signify anything ? i just do n't get it why she 'd do that . cheating but zoldycks must have a great time at thanksgiving.. .they went full free in the end . by far the best episode of this show. this was pure fun to watch from beginning to end . 'related : [ '' shounen sarutobi sasuke '' aka '' magic boy '' ] ( https : //www.youtube.com/watch ? v = yohgqmnskis )' uchuu senkan yamato looks interesting ! stop abandoning/tk'ing you griefer ) : [ time of eve ] ( http : //myanimelist.net/anime/7465/eve_no_jikan_movie ) has a very similar world and themes to ghost in the shell so you might like it . [ seirei no moribito ] ( http : //myanimelist.net/anime/1827/seirei_no_moribito ) is made by the same director as the ghost in the shell series and is a medieval fantasy just like berserk but not dark like berserk is. worth trying i think . if you just want a movie [ sword of the stranger ] ( http : //myanimelist.net/anime/2418/stranger__mukou_hadan ) is always good. basically a movie dedicated to showing off awesome sword fights and lots of blood ."

print find_tokens(sent)