"""
Presence taint analysis
"""
import numpy as np
import json
from flatten_dict import flatten

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
    influence_list = list()
    outputs = np.array(program(input_string))
    input_dict = json.loads(input_string)
    input_dict = flatten(input_dict)
    for i, (k, v) in input_dict.items():
        temp_input = input_dict.copy()
        del temp_input[k]
        abs_outpus = np.array(program(json.dumps(unflatten(temp_input))))
        influence = np.abs(outputs - abs_outputs)
        influence_list.append(influence)
    return influence_list
