"""
A module containing static variables for Hebrew language parsing.
"""

# Alphabetical characters
alphabet = 'אבגדהוזחטיכךלמםנןסעפףצץקרשת'

# shin and sin modifiers
shin = 'ׁ'
sin = 'ׂ'
shin_sin = shin + sin

# Nikkud
holam = 'ֹ'
shva = 'ְ'
dagesh = 'ּ'
other_kamatz = 'ׇ'              # used sometimes, unrecognized by Morfix
long_nikkud = ['ָ', 'ֵ']
short_nikkud = ['ַ', 'ֶ', 'ִ', 'ֻ']
reduced_nikkud = ['ֱ', 'ֲ ', 'ֳ']

nikud = [holam, shva, dagesh] + long_nikkud + short_nikkud + reduced_nikkud
nikud = ''.join(nikud)

# Including shin/sin for diacritics
diacritics = nikud + shin_sin