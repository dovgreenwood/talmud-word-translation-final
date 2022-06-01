from utils.jastrow_loader import *
from utils.deconstruct import *


def search_jastrow(words, lang='U', try_unvoweled=True):
    if lang == 'A':
        sub_dict = jas_aram
    elif lang == 'R':
        sub_dict = jas_heb
    elif lang == 'B':
        sub_dict = jas_bible
    else:
        sub_dict = jas_all

    all_rids = []
    for w in words:
        if w in sub_dict:
            all_rids += sub_dict[w]

    # None? try other languages
    if not all_rids:
        for w in words:
            if w in jas_all:
                all_rids += jas_all[w]

    if try_unvoweled and not all_rids:
        for w in words:
            no_vowel = alph_only(w)
            if no_vowel in sub_dict:
                all_rids += sub_dict[no_vowel]

        # Still none? try other languages without vowels
        if not all_rids:
            for w in words:
                no_vowel = alph_only(w)
                if no_vowel in jas_all:
                    all_rids += jas_all[no_vowel]

    return all_rids
