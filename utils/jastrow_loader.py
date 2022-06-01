import pickle

with open('utils/searchable_jastrow.pickle', 'rb') as f:
    jastrow = pickle.load(f)

jas_all = jastrow['R'] | jastrow['B'] | jastrow['A'] | jastrow['U']
jas_aram = jastrow['A'] | jastrow['U']
jas_bible = jastrow['B'] | jastrow['U']
jas_heb = jastrow['R'] | jastrow['U']