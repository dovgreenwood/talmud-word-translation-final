from utils import hebrew
import pickle
import re


# Map of prefix "bigrams" (counting only consonants) to substitute letters
with open('utils/prefixes.pickle', 'rb') as f:
    prefixes = pickle.load(f)


# Matches Hebrew prefix "bigrams"
prefix_matcher = '[' + hebrew.alphabet + '][' + hebrew.diacritics + ']*[' + \
                 hebrew.alphabet + '][' + hebrew.nikud + ']*'


all_verb_tags = ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'MD', 'VB-M')
all_noun_tags = ('NN', 'NNS', 'NNP', 'NNPS', 'NNG', 'NNGT', 'NNT')
morfix_pos_to_yap_pos = {
    'תואר': ('JJ', 'JJR', 'JJS', 'JJT'),
    'תואר הפועל': ('RB', 'RBR', 'RBS'),
    'מילת קישור': ('CC', 'IN'),
    'מילת קריאה': ('UH',),
    'מילת שאלה': ('HAM', 'QW', 'WDT'),
    'תחילית': ('Prefix',),
    'שֵם ז\'': all_noun_tags, 'שֵם נ\'': ('NN', 'NNS', 'NNP', 'NNPS'), 'שֵם': all_noun_tags,
    'מספר מונה': ('CDT', 'CD'), 'מספר סודר': ('CDT', 'CD'),
    'מילת יחס': ('IN',),
    'כינוי נפרד': ('PRP', 'PRP$'),
    'שֵם כמות': ('MOD',),
    '': 'Ambiguous',  # Can be shel, holiday, or other
    'פ\' קל': all_verb_tags, 'פ\' פיעל': all_verb_tags, 'פ\' הפעיל': all_verb_tags, 'פ\' התפעל': all_verb_tags,
    'פ\' נפעל': all_verb_tags, 'פ\' פועל': all_verb_tags, 'פ\' הופעל': all_verb_tags
}


def alph_only(token):
    return ''.join([c for c in token if c in hebrew.alphabet])


# Note that this method is slightly different from the former, in that it leaves punctuation
def remove_nikkud(token):
    return ''.join([c for c in token if not (1456 <= ord(c) <= 1479)])


def heb_plural(word, voweled=True):
    if voweled and word[-3:] == 'ִין':
        return word[:-1] + 'ם'
    elif word[-2:] == 'ין':
        return word[:-1] + 'ם'
    else:
        return word


def to_nitpael(word, voweled=True):
    if voweled and word[:4] == 'הִתְ':
        return 'נ' + word[1:]
    elif word[:2] == 'הת':
        return 'נ' + word[1:]
    else:
        return word


def to_hitpael(word, voweled=True):
    if voweled and word[:4] == 'נִתְ':
        return 'ה' + word[1:]
    elif word[:2] == 'נת':
        return 'ה' + word[1:]
    else:
        return word


def detach_prefixes(word, lang='U'):
    if lang == 'A':
        lang_prefixes = prefixes['A']
    elif lang == 'H':
        lang_prefixes = prefixes['H']
    else:
        lang_prefixes = prefixes['A'] | prefixes['H']

    possibilities = [word]

    while True:
        bigram = re.match(prefix_matcher, word)
        if bigram is None:
            break

        letters = bigram.group()
        if letters not in lang_prefixes:
            break

        new_start = bigram.span()[1]
        word = lang_prefixes[letters] + word[new_start:]
        possibilities.append(word)

    return possibilities
