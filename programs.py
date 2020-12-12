import json
import random

class program():
    def __init__(self, name=None, typ=None, input_length=None, output_length=None):
        self.name=name
        self.typ=typ
        self.input_length=input_length
        self.output_length=output_length

    def __call__(self, inps):
        if isinstance(inps[0], list):
            return self.run_many(inps)
        else:
            return self.run_one(inps)

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

    def gen_ref(self):
        # Defined in subclass
        pass

class FBD(program):
    def __init__(self):
        name = 'first_byte_dependent'
        typ = 'numeric'
        input_length = 2
        output_length = 1
        super(FBD, self).__init__(name, typ, input_length, output_length)

    def run_one(self, inps):
        a = inps[0]
        b = inps[1]
        c = 2 * a + b
        z = c - b
        return [z]

    def gen_input(self):
        return [random.random() for _ in range(self.input_length)]

    def gen_truth(self, inpt):
        return [[1.0], [0.0]]

    def gen_ref(self):
        return [[0.0], [0.0]]

class FBD2(program):
    def __init__(self):
        name = 'first_byte_dependent'
        typ = 'numeric'
        input_length = 2
        output_length = 1
        super(FBD, self).__init__(name, typ, input_length, output_length)

    def run_one(self, inps):
        a = inps[0]
        b = inps[1]
        c = 2 * a + b
        z = c - b
        return [z, z+b]

    def gen_input(self):
        return [random.random() for _ in range(self.input_length)]

    def gen_truth(self, inpt):
        return [[1.0], [0.0]]

    def gen_ref(self):
        return [[0.0, 1.0], [0.0, 1.0]]

class TBPD(program):
    def __init__(self):
        name = 'two_byte_partial_dependance'
        typ = 'numeric'
        input_length = 2
        super(TBPD, self).__init__(name, typ, input_length)

    def run_one(self, inps):
        a = inps[0]
        b = inps[1]
        c = a + a
        if (a < 0.5):
            z = c + b
        else:
            z = c
        return [z]

    def gen_input(self):
        return [random.random() for _ in range(self.input_length)]

    def gen_truth(self, inpt):
        return [[1.0], [1.0] if inpt[0] < 0.5 else [0.0]]

    def gen_ref(self):
        return [[0.6], [0.0]]

class JC(program):
    '''
    json_compare form: https://github.com/Akagi201/learning-python/blob/master/json/json_compare.py
    '''
    def __init__(self):
        name = 'json_compare'
        typ = 'string'
        input_length = 2
        super(JC, self).__init__(name, typ, input_length)
        self.json_item_num = 2
        self.json_key_length = 5
        self.json_value_length = 5
        import nltk
        from nltk.corpus import words
        nltk.download('words')
        self.words = [w for w in words.words() if len(w) <= 5]
        self.nums = [str(n) for n in range(9)]

    def ordered(self, obj):
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    def run_one(self, inpt):
        inpt_dict = json.loads(inpt)
        inps = list(inpt_dict.values())
        return [1.0] if self.ordered(inps[0]) == self.ordered(inps[1]) else [0.0]

    def gen_input(self):
        inpt1 = dict()
        inpt2 = dict()
        keys = random.sample(self.words, self.json_item_num*2)
        values = random.sample(self.words + self.nums, self.json_item_num*2)
        r = random.random()
        for i in range(self.json_item_num):
            inpt1[keys[i]] = values[i]
            i2 = i if r <= 0.5 else i+self.json_item_num
            inpt2[keys[i2]] = values[i2]
        return json.dumps({"input1": inpt1, "input2": inpt2})

    def gen_truth(self, inpt, taint_analysis='ptaint'):
        inpt_dict = json.loads(inpt)
        inps = list(inpt_dict.values())
        if taint_analysis == 'ptaint':
            if self.ordered(inps[0]) == self.ordered(inps[1]):
                return [[1.0], [1.0], [1.0], [1.0]]
            else:
                return [[0.0], [0.0], [0.0], [0.0]]
        else:
            return [[1.0], [1.0], [1.0], [1.0]]

    def gen_ref(self):
        ref1 = {
                ("input1", "0"*self.json_key_length): "."*self.json_value_length
                # for _ in range(self.json_item_num)
                }
        ref2 = {
                ("input1", "1"*self.json_key_length): ","*self.json_value_length
                }
        ref3 = {
                ("input2", "2"*self.json_key_length): "*"*self.json_value_length
                }
        ref4 = {
                ("input2", "3"*self.json_key_length): "#"*self.json_value_length
                }
        return [[ref1], [ref2], [ref3], [ref4]]

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
                and ("name" in d and isinstance(d["name"], str) and \
                len(d["name"]) > 0):
            return json.dumps({"person": d["name"], "howOld": d["age"], "somethingElse": random.randint(0, 10)})
    except:
        pass

    return 'Error'

