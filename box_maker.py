import sys
import string
from tqdm import tqdm
from itertools import permutations
import pickle

"""
perms = set(permutations([0,0,0,1,1,1,2,2,2,3,3,3]))
with open('box_perms.pickle', 'wb') as file:
    pickle.dump(perms, file)
"""

words = sys.argv[1:]
letters = ''.join(words)

uniq = list(set(letters))
uniq.sort()

def gen_perms(words):
    letters = ''.join(words)
    #letters = list(sys.argv[1])
    if len(set(letters)) > 12:
        print('Found too many letters ({})'.format(len(set(letters))))
        return
    elif len(set(letters)) < 12:
        print('Didn\'t find enough letters ({})'.format(len(set(letters))))
        return

    uniq = list(set(letters))
    uniq.sort()

    let_ind = {i:l for i,l in enumerate(uniq)}
    let_ind_rev = {l:i for i,l in enumerate(uniq)}

    restrictions = []
    for wrd in words:
        for i in range(len(wrd) - 1):
            restrictions.append([let_ind_rev[wrd[i]], let_ind_rev[wrd[i+1]]])

    #perm = permutations([0,0,0,1,1,1,2,2,2,3,3,3])
    with open('box_perms.pickle', 'rb') as file:
        perms = pickle.load(file)
    working_p = []

    for p in tqdm(perms):
        for i, j in restrictions:
            if p[i] == p[j]:
                break
        else:
            working_p.append(p)

    def perm_to_final(perm):
        tem = [[], [], [], []]
        for i, j in enumerate(perm):
            tem[j].append(let_ind[i])
        return tem

    good_perms = [perm_to_final(p) for p in working_p]
    for l in good_perms:
        l.sort()
    c = [''.join([''.join(m) for m in l]) for l in good_perms]
    good_perms = [[list(w[0:3]), list(w[3:6]), list(w[6:9]), list(w[9:12])] for w in set(c)]
    print('Found {} Possible Boxes'.format(len(good_perms)))
    return good_perms
gp = gen_perms(words)

alphabet = list(string.ascii_lowercase)
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

word_file = 'words.txt'

words = []
with open(word_file, 'r') as file:
    for line in file:
        words.append(line[:-1])

words = [word.lower() for word in words]
words = [word for word in words if word.isalpha()]

must_exc = [i for i in alphabet if i not in uniq]

new_words = []
for word in words:
    has_ex = False
    for char in must_exc:
        if char in word:
            has_ex = True
            break
    if not has_ex:
        new_words.append(word)

new_rmd = rmd(new_words)

def ows(ttt):
    return [w for w in ttt if len(set(w)) == len(uniq)]

def new_tws(ttt):
    to_check = {let:[w for w in ttt if w[0] == let] for let in alphabet}
    sols = []
    for w1 in ttt:
        for w2 in to_check[w1[-1]]:
            if len(set(w1 + w2)) == 12:
                sols.append([w1, w2])
    return sols

def find_solutions(box):
    ttt = rml(new_rmd, ml(box))
    one_word_solutions = ows(ttt)
    two_word_solutions = new_tws(ttt)
    return one_word_solutions, two_word_solutions

num_one_word = []
num_two_word = []
for box in tqdm(gp):
    a, b = find_solutions(box)
    num_one_word.append(a)
    num_two_word.append(b)
