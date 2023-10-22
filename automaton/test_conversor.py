'''
Basic test.
'''

from source.regex_fa import RegexToDFAConversor

RegexToDFAConversor.convert('a(a|b)*a')
