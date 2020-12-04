"""
Presence taint analysis
"""
import numpy as np
import json
from flatten_dict import flatten, unflatten

def ptaint_numeric(inputs, program, references):
    """
    ARGS:
        Inputs: list of numbers (ints, floats)
        program outputs: list of numbers
        references: a list of lists for each input
    Return:
        Influence: a list of arrays showing influence of each input on a all sinks (output)
    """
    influence_list = list()
    outputs = np.array(program(inputs))
    for i, inp in enumerate(inputs):
        abs_outputs = np.array([
            program(inputs[:i] + [ref] + inputs[i+1:]) for ref in references[i]
            ])
        influence = np.mean(np.abs(outputs - abs_outputs))
        influence_list.append(influence)
    return influence_list

def ptaint_string(input_string, program, references=None):

    """
    ARGS:
        Input: valid JSON string
        program outputs: list of numbers (ints, floats)
        references: a list of lists for each input (not implemented)
    Return:
        Influence: a list of arrays showing influence of each input on a all sinks (output)
    """

    def hamming_dist(str1, str2):
        count = np.abs(len(str1) - len(str2))

        for i in range(min(len(str1), len(str2))):
            if str1[i] != str2[i]:
                count += 1

        return count
    
    influence_list = list()
    outputs = program(input_string)
    input_dict = json.loads(input_string)
    input_dict = flatten(input_dict)
    temp_input = input_dict.copy()
    
    for i, (k, v) in enumerate(input_dict.items()):
        if references is None:
            del temp_input[k]
        elif k in references:
            temp_input[k] = references[k]
        else:
            del temp_input[k]
            
        abs_outputs = program(json.dumps(unflatten(temp_input)))
        influence = hamming_dist(abs_outputs, outputs)
        influence_list.append(influence)
        
        temp_input[k] = v

    if sum(influence_list) != 0:
        return [i / sum(influence_list) for i in influence_list]
    else:
        return influence_list
