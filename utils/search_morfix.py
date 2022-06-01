import requests
import json
from utils.deconstruct import *


def translate(word):
    if word == '':
        print('GOT IT')
        return []

    page = requests.get('http://services.morfix.com/translationhebrew/TranslationService/GetTranslation/' + word)
    data = json.loads(page.text)

    if data['ResultType'] == 'NoResult' or data['ResultType'] == 'Suggestions':
        word = heb_plural(word)
        page = requests.get('http://services.morfix.com/translationhebrew/TranslationService/GetTranslation/' + word)
        data = json.loads(page.text)

    if data['ResultType'] == 'NoResult' or data['ResultType'] == 'Suggestions':
        return []

    results = []
    for w in data['Words']:
        if w['PartOfSpeech'] in morfix_pos_to_yap_pos:
            pos = morfix_pos_to_yap_pos[ w['PartOfSpeech'] ][0]
        else:
            pos = w['PartOfSpeech']
            # print(w, '\t', pos)
        word = w['InputLanguageMeanings'][0][0]['DisplayText']
        results.append((word, pos))

    return results


def order_matches(responses, pos):
    return [w[0] for w in responses if w[1] == pos] + [w[0] for w in responses if w[1] != pos]
