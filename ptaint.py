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
        # influence = np.mean(np.abs(outputs - abs_outputs.T), axis=1)
        if len(references[i]) > 1:
            diff = np.ceil(np.abs(outputs - abs_outputs))
            influence = np.logical_and.reduce(diff, axis=0).astype(np.float)
        else:
            influence = np.abs(outputs - abs_outputs.T).squeeze(-1)
        influence_list.append(influence)
    return influence_list

def ptaint_string(input_string, program, references=None):

    """
    ARGS:
        Input: valid JSON string
        program: outputs list of numbers (ints, floats)
        references: a list of lists for each input
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

        del temp_input[k]
        dist = [1.0 for _ in range(len(outputs))]
        for input_ref in references[i]:
            temp_input.update(input_ref)
            abs_outputs = program(json.dumps(unflatten(temp_input)))
            if isinstance(abs_outputs[0], str):
                dist = [
                        int(dist[i]) & int(hamming_dist(abs_output, output))
                        for i, (abs_output, output) in
                        enumerate(zip(abs_outputs, outputs))
                        ]
            else:
                dist = [
                        int(dist[i]) & int(abs(output - abs_output))
                        for i, (abs_output, output) in
                        enumerate(zip(abs_outputs, outputs))
                        ]

            _ = temp_input.popitem()

        influence_list.append(dist)

        temp_input[k] = v

    return influence_list
