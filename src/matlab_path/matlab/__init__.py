import logging

from textmate_grammar.grammars import matlab
from textmate_grammar.language import LanguageParser
from textmate_grammar.utils import cache

logging.getLogger("textmate_grammar").setLevel(logging.ERROR)
cache.init_cache("shelve")

TM_PARSER = LanguageParser(matlab.GRAMMAR)
