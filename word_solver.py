import sys
import string
from tqdm import tqdm

word_file = 'words.txt'

words = []
with open(word_file, 'r') as file:
    for line in file:
        words.append(line[:-1])

words = [word.lower() for word in words]
words = [word for word in words if word.isalpha()]

inc = list(sys.argv[1])
try:
    must_inc = list(sys.argv[2])
except:
    must_inc = []

if inc[0] == '-':
    inc = list(string.ascii_lowercase)

alphabet = list(string.ascii_lowercase)
must_exc = [i for i in alphabet if i not in inc]

new_words = []
for word in words:
    dnh_must_inc = False
    for l in must_inc:
        if l not in word:
            dnh_must_inc = True
            break
    if dnh_must_inc:
        continue
    has_ex = False
    for char in must_exc:
        if char in word:
            has_ex = True
            break
    if not has_ex:
        new_words.append(word)

def greater(num, l):
	return [i for i in l if len(i) > num]

def lesser(num, l):
	return [i for i in l if len(i) < num]

double_letters = [(i + i) for i in alphabet]

def rmd(l):
	tt = l
	for pair in double_letters:
		tt = [word for word in tt if pair not in word]
	return tt

def rml(l, p):
	tt = l
	for pair in p:
		tt = [word for word in tt if pair not in word]
	return tt

def ml(l):
	tt = []
	for w in l:
		tt.append(w[0] + w[1])
		tt.append(w[0] + w[2])
		tt.append(w[1] + w[0])
		tt.append(w[1] + w[2])
		tt.append(w[2] + w[0])
		tt.append(w[2] + w[1])
	return tt

def ml2():
	l = [inc[0:3], inc[3:6], inc[6:9], inc[9:12]]
	return ml(l)

def ows(ttt):
    return [w for w in ttt if len(set(w)) == len(inc)]

def new_tws(ttt):
    to_check = {let:[w for w in ttt if w[0] == let] for let in alphabet}
    sols = []
    for w1 in tqdm(ttt):
        for w2 in to_check[w1[-1]]:
            if len(set(w1 + w2)) == 12:
                sols.append([w1, w2])
    return sols

def tws(ttt):
    sols = []
    for i in tqdm(range(len(ttt))):
        for j in range(i+1, len(ttt)):
            w1 = ttt[i]
            w2 = ttt[j]
            if len(set(w1 + w2)) == 12:
                if w1[-1] == w2[0]:
                    sols.append([w1, w2])
                if w1[0] == w2[-1]:
                    sols.append([w2, w1])
    return sols

def btws(sols, theta = 0):
    sol_lens = [len(s[0]) + len(s[1]) for s in sols]
    min_sol_len = min(sol_lens)
    return [sols[i] for i in range(len(sol_lens)) if sol_lens[i] == min_sol_len + theta]

if len(inc) == 12:
    ttt = rml(rmd(new_words), ml2())
    one_word_solutions = ows(ttt)
    if len(one_word_solutions) > 0:
        print('Found a 1-word solution!')
    two_word_solutions = new_tws(ttt)
    print('Found {} 2-word solutions!'.format(len(two_word_solutions)))
    best_two_word = btws(two_word_solutions)
else:
    ttt = [word for word in new_words if len(word) > 3]
    one_word_solutions = ows(ttt)
