import json
import time
import random

class program():
    def __init__(self, name=None, typ=None, input_length=None):
        self.name=name
        self.typ=typ
        self.input_length=input_length

    def __call__(self, inps):
        if isinstance(inps[0], list):
            return self.run_one(inps)
        else:
            return self.run_many(inps)

    def run_many(self, inps):
        return [self.run_one(n) for n in inps]

    def gen_inputs(self, k):
        return [self.gen_input() for _ in range(k)]

    def gen_truths(self, inps):
        return [self.gen_truth(n) for n in inps]

    def run_one(self, inps):
        # Defined in subclass
        pass

    def gen_input(self):
        # Defined in subclass
        pass

    def gen_truth(self, inpt):
        # Defined in subclass
        pass

class FBD(program):
    def __init__(self):
        name = 'first_byte_dependent'
        typ = 'numeric'
        input_length = 2
        super(FBD, self).__init__(name, typ, input_length)

    def run_one(self, inps):
        a = inps[0]
        b = inps[1]
        c = 2 * a + b
        z = c - b
        return z

    def gen_input(self):
        return [random.random() for _ in range(self.input_length)]

    def gen_truth(self, inpt):
        return [1.0, 0.0]

class TBPD(program):
    def __init__(self):
        name = 'two_byte_partial_dependance'
        typ = 'numeric'
        input_length = 2
        super(FBD, self).__init__(name, typ, input_length)

    def run_one(self, inps):
        a = inps[0]
        b = inps[1]
        c = a + a
        if (a < 0.5):
            z = c + b
        else:
            z = c
        return z

    def gen_input(self):
        return [random.random() for _ in range(self.input_length)]

    def gen_truth(self, inpt):
        return [1.0, 1.0 if inpt[0] < 0.5 else 0.0]

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

