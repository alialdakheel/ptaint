"""
    Compare ptaint to neutaint

    TODO:
        - Prepare ground truth for any input for each of programs
        - run both ptaint & neutaint on many inputs
        - compute errors
        - compare run time
"""
from math import isclose
import numpy as np
import programs
import ptaint
from util import run_neutaint

class Evaluation():
    """
    Takes a list of programs to evaluate on
    """
    def __init__(self, program_list, dataset_length=1000):
        self.program_names = program_list
        self.dataset_length = dataset_length

        self.program_insts = [
                getattr(programs, p)() for p in self.program_names
                ]
        self.input_datasets = [
                self.construct_dataset(inst) for inst in self.program_insts
                ]
        self.ground_truths = [
                p.gen_truths(self.input_datasets[i]) for
                i, p in enumerate(self.program_insts)
                ]
        self.refs = [p.gen_ref() for p in self.program_insts]

        # self.ptaint_numeric_results = self.evaluate_ptaint_numeric()
        self.ptaint_numeric_results = self.evaluate_taint(ptaint.ptaint_numeric)

    def construct_dataset(self, inst):
        return inst.gen_inputs(self.dataset_length)

    def compute_errors(self, results, truth):
        res = np.array(results)
        tru = np.array(truth)
        return np.mean(np.abs(tru - results))


    def evaluate_ptaint_numeric(self):
        self.results_list = list()
        for i, (p, ref) in enumerate(zip(self.program_insts, self.refs)):
            results = list()
            for inpt in self.input_datasets[i]:
                inf = ptaint.ptaint_numeric(inpt, p, ref)
                result = [0.0 if isclose(v, 0.0, abs_tol=1e-14) else 1.0 for v in inf]
                results.append(result)
            self.results_list.append(results)
        eval_result = [
                self.compute_errors(r, t) for
                r, t in zip(self.results_list, self.ground_truths)
                    ]

        return eval_result

    def evaluate_taint(self, method, need_refs=True):
        self.results_list = list()
        for i, (p, ref) in enumerate(zip(self.program_insts, self.refs)):
            results = list()
            for inpt in self.input_datasets[i]:
                if need_refs:
                    taint_args=[inpt, p, ref]
                else:
                    taint_args=[inpt, p]
                inf = method(*taint_args)
                # print(inf, isclose(inf[1], 0.0, abs_tol=1e-14))
                result = [0.0 if isclose(v, 0.0, abs_tol=1e-14) else 1.0 for v in inf]
                results.append(result)
            self.results_list.append(results)
        eval_result = [
                self.compute_errors(r, t) for
                r, t in zip(self.results_list, self.ground_truths)
                    ]
        return eval_result


if __name__ == "__main__":
    program_list = [
            'FBD',
            'TBPD'
            ]
    dataset_length = 100
    ev = Evaluation(program_list, dataset_length=dataset_length)
    for i, program in enumerate(program_list):
        print(f"program: {program}, ptaint_numeric_error_rate: {ev.ptaint_numeric_results[i]}")

