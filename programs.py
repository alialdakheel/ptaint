import json
import time
import random


def first_byte_dependent(input):
    x = input
    a = x[0]
    b = x[1]
    c = a * a + b
    z = c - b
    return z

def two_byte_partial_dependance(input):
    x = input
    a = x[0]
    b = x[1]
    c = a + a
    if (a < 0.5):
        z = c + b
    else:
        z = c
    return z


def first_byte_value_dependent(input):
    x = input
    if x[0] == 0.5:
        return 1
    return 0


def key_swap(query_params):
    # a program json -> json where values may be passed from input to output
    # into new keys. the key mapping, if any, is not known.
    try:
        d = json.loads(query_params.strip())
        if ("age" in d and isinstance(d["age"], int) and d["age"] > 0) \
                and ("name" in d and isinstance(d["name"], str) and len(
            d["name"]) > 0):
            return json.dumps({"person": d["name"], "howOld": d["age"], "somethingElse": random.randint(0, 10)})
    except:
        return "Error"

