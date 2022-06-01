import json
from utils import cachemanager, deconstruct, search_morfix, direct_search, jastrow_loader
import pickle
import os

with open('word-maps/all_bdb_to_jastrow.pickle', 'rb') as f:
    bdb_to_jas = pickle.load(f)
    bdb_no_nik = {deconstruct.alph_only(w): bdb_to_jas[w] for w in bdb_to_jas}
with open('word-maps/all_dicta_to_jastrow.pickle', 'rb') as f:
    dicta_to_jas = pickle.load(f)
    dicta_no_nik = {deconstruct.alph_only(w): dicta_to_jas[w] for w in dicta_to_jas}
with open('word-maps/all_pealim_to_jastrow.pickle', 'rb') as f:
    pealim_to_jas = pickle.load(f)
cachemanager.load_hebrew('utils/heb_cache.csv')

shortcuts = {
    'מַתְנִי׳': 'M03094',
    'גְּמָ׳': 'C01067',
    'x': '',
}


def translate_hebrew(word, pos, from_aram=False):
    # try maleh spelling in cache and pealim
    possibilities = deconstruct.detach_prefixes(word[1], 'H')
    for token in possibilities:
        if token in cachemanager.heb_cache:
            return cachemanager.heb_cache[token]
        if token in pealim_to_jas:
            return pealim_to_jas[token]

    # try haser spelling in cache and pealim
    possibilities = deconstruct.detach_prefixes(word[2], 'H')
    for token in possibilities:
        if token in cachemanager.heb_cache:
            return cachemanager.heb_cache[token]
        if token in pealim_to_jas:
            return pealim_to_jas[token]

    # try maleh spelling in Morfix
    morfix_results = search_morfix.translate( deconstruct.alph_only(word[1]) )
    morfix_results = search_morfix.order_matches(morfix_results, pos)
    morfix_results = direct_search.search_jastrow(word + morfix_results, 'R')

    # try haser spelling in morfix
    if not morfix_results:
        morfix_results = search_morfix.translate( deconstruct.alph_only(word[2]) )
        morfix_results = search_morfix.order_matches(morfix_results, pos)
        morfix_results = direct_search.search_jastrow(word + morfix_results, 'R')

    # save Morfix results to cache
    cachemanager.add_to_cache(word[1], list(set(morfix_results)))

    # ensures there won't be an infinite Hebrew<->Aramaic loop
    if morfix_results:
        return morfix_results
    elif from_aram:
        return []
    else:
        return translate_aramaic(word, from_heb=True)  # in case the language was misidentified


def translate_aramaic(word, from_heb=False):
    # start with haser spelling, which is what the Dicta database usually uses
    possibilities_haser = deconstruct.detach_prefixes(word[2], 'A')

    for token in possibilities_haser:
        if token in dicta_to_jas:
            return dicta_to_jas[token]

    # now try maleh
    possibilities_maleh = deconstruct.detach_prefixes(word[1], 'A')

    for token in possibilities_maleh:
        if token in dicta_to_jas:
            return dicta_to_jas[token]

    # try without nikud, starting with haser -- TODO: IS THERE AN ERROR HERE OF LOOKING UP LETTERS?
    possibilities_noalph = [deconstruct.alph_only(w) for w in possibilities_haser]
    for token in possibilities_noalph:
        if token in dicta_no_nik:
            return dicta_no_nik[token]

    # now with maleh
    possibilities_noalph = [deconstruct.alph_only(w) for w in possibilities_maleh]
    for token in possibilities_noalph:
        if token in dicta_no_nik:
            return dicta_no_nik[token]

    # try a direct search using the haser spelling
    direct_results = direct_search.search_jastrow(possibilities_haser, 'A')

    # try a direct search using the maleh spelling
    if not direct_results:
        direct_results = direct_search.search_jastrow(possibilities_maleh, 'A')

    # ensures there won't be an infinite Hebrew<->Aramaic loop
    if direct_results:
        return direct_results
    elif from_heb:
        return []
    else:
        return translate_hebrew(word, 'xxx', from_aram=True)


def translate_bible(word):
    if word[1] in bdb_to_jas:
        return bdb_to_jas[word[1]]
    elif word[2] in bdb_to_jas:
        return bdb_to_jas[word[2]]

    no_alph = [deconstruct.alph_only(w) for w in word]
    if no_alph[1] in bdb_no_nik:
        return bdb_no_nik[no_alph[1]]
    elif no_alph[2] in bdb_no_nik:
        return bdb_no_nik[no_alph[2]]

    direct_results = direct_search.search_jastrow(word[1], 'B')
    if not direct_results:
        direct_results = direct_search.search_jastrow(word[2], 'B')
    return direct_results if direct_results else translate_hebrew(word, 'xxx')


files = os.listdir('data/pos_tagged_talmud/')

if __name__ == '__main__':
    for file in files:
        title = file[:-5]
        do_masekhet = input('Proceed with ' + title + '? y/n: ')
        if do_masekhet == 'n':
            continue

        with open('data/pos_tagged_talmud/' + file, encoding='utf-8') as f:
            text = json.load(f)

        output = []
        i = 0
        for p in text:
            print('===================\n', i, '/', len(text), '\n===================')
            output.append([])
            for c in p:
                output[-1].append([])
                for w in c:
                    lang = w['lang']
                    word = w['word']
                    print(word)
                    if word[1] in shortcuts:
                        output[-1][-1].append({word[0]: [shortcuts[word[1]]]})
                    elif lang == 'A':
                        output[-1][-1].append({word[0]: list(set(translate_aramaic(word)))})
                    elif lang == 'B':
                        output[-1][-1].append({word[0]: list(set(translate_bible(word)))})
                    elif lang == 'R':
                        output[-1][-1].append({word[0]: list(set(translate_hebrew(word, w['pos'])))})
                    else:
                        direct_results = direct_search.search_jastrow(word)
                        if direct_results:
                            output[-1][-1].append({word[0]: list(set(direct_results))})
                        else:
                            output[-1][-1].append({word[0]: list(set(translate_aramaic(word) +
                                                                     translate_hebrew(word, w['pos']) +
                                                                     translate_bible(word)))})
                    print(lang, ' ', output[-1][-1][-1], '\n')
            i += 1

        with open('data/final_talmud/' + file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

    cachemanager.save_hebrew('utils/heb_cache.csv')
