from feedoo_hash.abstract_filter_hash import AbstractFilterHash
import hashlib

# MD5 sum of a key

class FilterSha512(AbstractFilterHash):
    def __init__(self, match, key, output_key):
        AbstractFilterHash.__init__(self, match, key, output_key, hashlib.sha251)








