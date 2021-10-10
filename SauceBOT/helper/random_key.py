import random
import string


def rankey(range_digit=5, abc123=string.hexdigits):
    return "".join([random.choice(abc123) for i in range(range_digit)])
